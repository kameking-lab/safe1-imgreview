# -*- coding: utf-8 -*-
"""
pptx2pdf_com.py — PowerPoint COM で pptx を PDF に書き出す（LibreOffice不在のため）。
Chrome 不可侵・既存ファイル非破壊（出力PDFは新ファイル名）。
使い方: py pptx2pdf_com.py <in.pptx> <out.pdf>
"""
import os
import sys
import win32com.client

PP_PDF = 32  # ppSaveAsPDF


def main():
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    assert os.path.exists(src), src
    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = None
    try:
        pres = app.Presentations.Open(src, WithWindow=False)
        pres.SaveAs(dst, PP_PDF)
        print("PDF_SAVED", dst, "bytes:", os.path.getsize(dst))
    finally:
        if pres is not None:
            pres.Close()
        app.Quit()


if __name__ == "__main__":
    main()
