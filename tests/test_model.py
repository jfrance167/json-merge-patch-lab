import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from merge_lab.contract import LabError, Unsupported, parse, validate, _walk
from merge_lab.model import analyze, render

ROOT=Path(__file__).resolve().parents[1]
ORACLES=json.loads((ROOT/"fixtures/oracles.json").read_text(encoding="ascii"))


def envelope(target=None, patch=None, schema="merge-patch-lab/1"):
    return {"schema":schema,"target":target,"patch":patch}


def wire(value):
    return json.dumps(value,ensure_ascii=False).encode("utf-8")


class ModelTests(unittest.TestCase):
    def test_frozen_reports(self):
        self.assertEqual(hashlib.sha256((ROOT/"fixtures/oracles.json").read_bytes()).hexdigest(),
                         "4a9afc1eb0e5a9ac9eeb1fa570e9e84290017089a898c6b7032495e082587c77")
        self.assertGreaterEqual(len(ORACLES["cases"]),32)
        for case in ORACLES["cases"]:
            with self.subTest(name=case["name"]):
                source=copy.deepcopy(case["input"])
                report,code=analyze(parse(wire(source)))
                self.assertEqual(report,case["expected"])
                self.assertEqual(code,case["exit"])
                self.assertEqual(source,case["input"])
                self.assertEqual(json.loads(render(report)),report)

    def test_null_deletion(self):
        report,code=analyze(envelope({"gone":False,"keep":None},{"gone":None,"absent":None}))
        self.assertEqual(report["result"],{"keep":None})
        self.assertEqual(code,1)

    def test_array_replacement(self):
        report,_=analyze(envelope([1,2],[None,{"n":None}]))
        self.assertEqual(report["result"],[None,{"n":None}])

    def test_object_on_scalar(self):
        report,_=analyze(envelope(0,{"new":2}))
        self.assertEqual(report["result"],{"new":2})

    def test_exact_names(self):
        report,_=analyze(envelope({"\u00e9":1,"e\u0301":2},{"e\u0301":3}))
        self.assertEqual(report["result"],{"\u00e9":1,"e\u0301":3})

    def test_detached_snapshots(self):
        target={"old":[]}
        patch_value=[{"nested":[]}]
        report,_=analyze(envelope(target,patch_value))
        report["result"][0]["nested"].append(1)
        self.assertEqual(patch_value,[{"nested":[]}])
        self.assertEqual(report["patch"],[{"nested":[]}])
        report["target"]["old"].append(2)
        self.assertEqual(target,{"old":[]})
        report["patch"][0]["nested"].append(3)
        self.assertEqual(report["result"],[{"nested":[1]}])

    def test_cross_source_aliases(self):
        shared={"x":[]}
        source=envelope({"a":shared,"b":shared},{"c":shared})
        report,_=analyze(source)
        report["result"]["a"]["x"].append(1)
        self.assertEqual(shared,{"x":[]})
        self.assertEqual(report["result"]["b"],{"x":[]})
        self.assertEqual(report["result"]["c"],{"x":[]})

    def test_typed_change_and_order(self):
        for target,value in ((False,0),(0,False),({"x":False},{"x":0})):
            report,code=analyze(envelope(target,value))
            self.assertIs(report["changed"],True)
            self.assertEqual(code,1)
        self.assertEqual(analyze(envelope({"a":1,"b":2},{"b":2,"a":1}))[1],0)
        self.assertEqual(analyze(envelope([0,1],[1,0]))[1],1)
        self.assertEqual(render(analyze(envelope({"b":2,"a":1},{}))[0]),
                         render(analyze(envelope({"a":1,"b":2},{}))[0]))

    def test_secondary_idempotence(self):
        for case in ORACLES["cases"]:
            first,_=analyze(case["input"])
            second,code=analyze(envelope(first["result"],case["input"]["patch"]))
            self.assertEqual(second["result"],case["expected"]["result"])
            self.assertEqual(code,0)

    def test_no_hooks_before_rejection(self):
        calls=[]

        class Meta(type):
            def __eq__(self,other):
                calls.append("equality")
                raise RuntimeError("hook")

        class Foreign(metaclass=Meta):
            def __iter__(self):
                calls.append("iteration")
                raise RuntimeError("hook")

            def __deepcopy__(self,_memo):
                calls.append("copy")
                raise RuntimeError("hook")

        class DictSubclass(dict):
            def items(self):
                calls.append("items")
                raise RuntimeError("hook")

        class TextSubclass(str):
            def __hash__(self):
                calls.append("hash")
                return 0

        key=TextSubclass("name")
        keyed={key:0}
        calls.clear()
        for value in (Foreign(),DictSubclass(),TextSubclass("value"),keyed):
            self.assertRaises(LabError,analyze,envelope(value,None))
            self.assertRaises(LabError,analyze,envelope(None,value))
        self.assertEqual(calls,[])

    def test_cycles(self):
        cycle=[]
        cycle.append(cycle)
        self.assertRaises(LabError,analyze,envelope(cycle,{}))
        self.assertRaises(LabError,analyze,envelope(None,cycle))
        source=envelope()
        source["target"]=source
        self.assertRaises(LabError,analyze,source)

    def test_full_branch_admission_and_support_precedence(self):
        for source in (envelope({"drop":float("nan")},{"drop":None}),
                       envelope({"drop":"\ud800"},None,"unknown/1"),
                       envelope(0,{"bad":object()},"unknown/1")):
            with patch("merge_lab.model._merge") as merge:
                self.assertRaises(LabError,analyze,source)
                merge.assert_not_called()
        for case in ORACLES["errors"]:
            with self.subTest(name=case["name"]),self.assertRaises(LabError) as caught:
                analyze(parse(case["raw"].encode("ascii")))
            self.assertEqual(str(caught.exception),case["diagnostic"]["reason"])
            self.assertEqual(isinstance(caught.exception,Unsupported),case["exit"]==3)

    def test_lexical_before_decoder(self):
        for raw in (b"["*9+b"0"+b"]"*9,b"9"*33,b"1e2",b"1.0",b"-0",b"9007199254740992"):
            with self.subTest(raw=raw),patch("merge_lab.contract.json.loads") as loads:
                self.assertRaises(LabError,parse,raw)
                loads.assert_not_called()
        self.assertEqual(analyze(parse(wire(envelope("["*64+"9"*64,{}))))[0]["result"],{})

    def test_json_and_shapes(self):
        for raw in (b"\xff",b"\xef\xbb\xbf{}",b"{}{}",b"NaN",b"Infinity",b"01",b"-01",b'{"x":1,"\\u0078":2}'):
            self.assertRaises(LabError,parse,raw)
        self.assertRaises(LabError,parse,bytearray(b"{}"))
        for value in ([],{}, {**envelope(),"extra":0},{"schema":"merge-patch-lab/1","patch":None}):
            self.assertRaises(LabError,analyze,value)
        for schema in ("","a"*65,"bad space","\u00e9"):
            self.assertRaises(LabError,analyze,envelope(schema=schema))

    def test_integer_bounds_and_types(self):
        for value in (-9007199254740991,9007199254740991):
            self.assertEqual(analyze(parse(wire(envelope(0,value))))[0]["result"],value)
        for value in (9007199254740992,-9007199254740992,1.0):
            self.assertRaises(LabError,analyze,envelope(0,value))

    def test_raw_byte_boundary(self):
        raw=wire(envelope())
        parse(raw+b" "*(32768-len(raw)))
        self.assertRaises(LabError,parse,raw+b" "*(32769-len(raw)))

    def test_tree_nodes_containers_and_alias_counts(self):
        validate(envelope([0]*511,None))
        self.assertRaises(LabError,validate,envelope([0]*512,None))
        validate(envelope([[] for _ in range(63)],None))
        self.assertRaises(LabError,validate,envelope([[] for _ in range(64)],None))
        shared=[0]*255
        self.assertRaises(LabError,validate,envelope([shared,shared],None))

    def test_depth_and_global_pre_shape_bounds(self):
        value=0
        for _ in range(7):
            value=[value]
        validate(envelope(value,None))
        self.assertRaises(LabError,validate,envelope([value],None))
        _walk([0]*1025,"global")
        self.assertRaises(LabError,_walk,[0]*1026,"global")
        _walk([[] for _ in range(128)],"global")
        self.assertRaises(LabError,_walk,[[] for _ in range(129)],"global")

    def test_text_scalar_and_aggregate_bounds(self):
        validate(envelope("\U0001f600"*128,None))
        self.assertRaises(LabError,validate,envelope("a"*129,None))
        validate(envelope(["a"*128]*16,None))
        self.assertRaises(LabError,validate,envelope(["a"*128]*16+["a"],None))
        _walk(["a"*1024]*5,"global")
        self.assertRaises(LabError,_walk,["a"*1024]*5+["a"],"global")
        for value in ("\ud800","\ufdd0","\ufffe","\U0001ffff"):
            self.assertRaises(LabError,analyze,envelope(value,None))
        validate(envelope("\u0000\u200b\ue000\u0378",None))

    def test_output_amplification(self):
        source=ORACLES["overflow"]["input"]
        self.assertLess(len(wire(source)),32768)
        report,code=analyze(parse(wire(source)))
        self.assertEqual(code,1)
        self.assertEqual(len(report["result"]),64)
        raw= (json.dumps(report,ensure_ascii=True,sort_keys=True,separators=(",",":"))+"\n").encode("ascii")
        self.assertGreater(len(raw),65536)
        self.assertLess(len(raw),131072)
        with self.assertRaises(LabError) as caught:
            render(report)
        self.assertEqual(str(caught.exception),"resource limit")

    def test_exact_output_cap(self):
        self.assertEqual(len(render("a"*65533).encode("ascii")),65536)
        self.assertRaises(LabError,render,"a"*65534)


if __name__=="__main__":
    unittest.main()
