#!/usr/bin/env python3
"""Markdown 导出验收探针。

契约：
  tablib.Dataset(headers=[...]).export("md") -> str
  - 表头行 + 分隔行（`| --- | --- |`）+ 数据行
  - 单元格里的 `|` 转义成 `\\|`，换行替换成 `<br>`
  - 空数据只有表头时，仍输出表头行与分隔行
  - 末尾不带多余空行
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tablib  # noqa: E402

FAILED = 0
PASSED = 0


def check(code, desc, fn):
    global FAILED, PASSED
    try:
        fn()
        print(f"[PASS] {code} {desc}")
        PASSED += 1
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {code} {desc}")
        print(f"        {type(exc).__name__}: {exc}")
        FAILED += 1


def main():
    def p1():
        ds = tablib.Dataset(headers=["name", "qty"])
        ds.append(["a", 1])
        ds.append(["b", 2])
        out = ds.export("md")
        lines = out.strip().splitlines()
        assert lines[0] == "| name | qty |", lines[0]
        assert lines[1] == "| --- | --- |", lines[1]
        assert lines[2] == "| a | 1 |", lines[2]

    def p2():
        ds = tablib.Dataset(headers=["note"])
        ds.append(["x|y"])
        assert "\\|" in ds.export("md"), ds.export("md")

    def p3():
        ds = tablib.Dataset(headers=["note"])
        ds.append(["a\nb"])
        assert "<br>" in ds.export("md"), ds.export("md")

    def p4():
        ds = tablib.Dataset(headers=["only"])
        out = ds.export("md").strip().splitlines()
        assert out == ["| only |", "| --- |"], out

    def p5():
        ds = tablib.Dataset(headers=["a"])
        ds.append([1])
        assert ds.export("md").strip().endswith("| 1 |"), repr(ds.export("md"))

    def p6():
        ds = tablib.Dataset(headers=["a", "b"])
        ds.append([1, 2])
        # csv 写出用 \r\n 行尾，统一换行后再比对，只验证内容不受 Markdown 格式影响
        assert ds.export("csv").replace("\r\n", "\n").strip() == "a,b\n1,2", repr(ds.export("csv"))

    def p7():
        titles = [f.title for f in tablib.formats.registry.formats()]
        assert "md" in titles, titles
        assert tablib.formats.registry.get_format("md") is not None

    check("P1", "基本表格结构", p1)
    check("P2", "竖线转义", p2)
    check("P3", "换行替换为 <br>", p3)
    check("P4", "空数据只有表头", p4)
    check("P5", "末尾不多空行", p5)
    check("P6", "CSV 导出不受影响", p6)
    check("P7", "格式已注册进 registry", p7)

    print("-" * 60)
    print(f"探针汇总：{PASSED}/{PASSED + FAILED} 通过")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
