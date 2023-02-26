import sys
import re
import logging
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from IPython.display import display as _display
from IPython.display import Image as _Image
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass

logging.getLogger("numexpr").setLevel(logging.WARNING)
# tabulate.PRESERVE_WHITESPACE = True


class RvTextUtf:
    """convert rivt-string to UTF8 calc"""

    def __init__(self):

        # _rgx = r"\[([^\]]+)]_"  # find tags

        a = 1

    def r_utf(self, strL, folderD, incrD):
        """process rivt string to utf

        :param list strL: split rivt string
        :param dict folderD: folder paths
        :param dict incrD: format numbers that increment
        :return string rvtS: utf string
        """

        self.strL = strL
        self.folderD = folderD
        self.incrD = incrD

        cmdL = ["project", "github", "append"]
        tagL = ["_[new]", "_[url]", "_[[readme]]", "_[[end]]"]

        # get valid commands

        for uS in self.strL:
            if uS[0:2] == "##":
                continue  # remove review comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                print(" ")
                self.calcS += "\n"
                continue
            try:
                if uS[0] == "#":
                    continue  # remove comment
            except:
                print(" ")  # if uS[0] throws error
                self.calcS += "\n"
                continue

            self.utfS += uS.rstrip() + "\n"

        return rvtS, self.calcS, self.incrD

    def i_utf(self, strL, folderD, incrD):
        """convert insert-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD

    def v_utf(self, strL, folderD, incrD, localD):
        """convert value-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
            vL (list): configuration parameters
        """

        locals().update(self.rivtD)
        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()
        # write dictionary from value-string
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                val1U = val2U = array(eval(valS))
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:  # no units
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            utfS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"
            utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            print("\n" + utfS + "\n")  # pretty print equation
            self.calcS += "\n" + utfS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:  # substitute into equation
                self._vsub(vL)
            else:  # write equation table
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

        # update dictionary
        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

        # assign values
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            rstS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty print
            symeq = sp.sympify(spS, _clash2, evaluate=False)
            eqltxS = sp.latex(symeq, mul_symbol="dot")
            self.restS += "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL, fltfmtS)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                # print(f"{cmdS=}")
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())
        # print(self.rivtD)

        # write values to table
        tbl = "x"
        hdrL = "y"
        tlbfmt = "z"
        alignL = "true"
        fltfmtS = "x"
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        tableS = tabulate(
            tbl,
            tablefmt=tblfmt,
            headers=hdrL,
            showindex=False,
            colalign=alignL,
            floatfmt=fltfmtS,
        )
        output.write(tableS)
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        inrstS = ""
        self.restS += ":: \n\n"
        for i in rstS.split("\n"):
            inrstS = "  " + i
            self.restS += inrstS + "\n"
        self.restS += "\n\n"
        self.rivtD.update(locals())

    if vsub:
        eqL = [1]
        eqS = "descrip"
        locals().update(self.rivtd)

        eformat = ""
        utfS = eqL[0].strip()
        descripS = eqL[3]
        parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try:
            eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
            # sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            self.calcl.append(utfs)
        except:
            self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())  # substitute
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, "~")
                new_var = new_var.replace("_", "|")
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            # print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
            for _n1 in symat1:
                orig_var = str(_n1).replace("~", "")
                orig_var = orig_var.replace("|", "_")
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = "{:." + eformat + "f}"
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            # print('out2b\n', out2)
            out3 = out2  # clean up unicode
            out3.replace("*", "\\u22C5")
            # print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == "-":
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                    _cnt = 0
        except:
            pass

    def t_utf(self,  trL, folderD, incrD, localD):
        """convert table-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        locals().update(self.rivtD)
        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD


class RvTextRest:
    """convert rivt-strings to reST strings

    Args:
    exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    tagD (dict): tag dictionary


    """

    def __init__(self, strL: list, folderD: dict, tagD: dict):

        self.restS = """"""  # restructured text string
        self.strL = strL  # rivt-string list
        self.folderD = folderD
        self.tagD = tagD
        strL: list,
        folderD: dict,
        setcmdD: dict,
        setsectD: dict,
        rivtD: dict,
        exportS: str,
        self.restS = """"""  # restructured text string
        self.exportS = exportS  # value export string
        self.strL = strL  # rivt-string list
        self.valL = []  # value blocklist
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivtD = rivtD

    def r_rst(self, typeS: str, cmdL: list, methL: list, tagL: list):
        """parse rivt-string to reST

        Args:
            typeS (str): rivt-string type
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        locals().update(self.rivtD)
        uL = []  # command arguments
        indxI = -1  # method index
        _rgx = r"\[([^\]]+)]_"  # find tags

        for uS in self.strL:
            if uS[0:2] == "##":
                continue  # remove comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                if len(self.valL) > 0:  # print value table
                    fltfmtS = ""
                    hdrL = ["variable", "value", "[value]", "description"]
                    alignL = ["left", "right", "right", "left"]
                    self._vtable(self.valL, hdrL, "rst", alignL, fltfmtS)
                    self.valL = []
                    self.restS += "\n\n"
                    self.rivtvalD.update(locals())
                    continue
                else:
                    # self.restS += "?x?vspace{7pt}"
                    self.restS += "\n"
                    continue
            try:
                if uS[0] == "#":
                    continue  # remove comment
            except:
                self.restS += "\n"
                continue
            if uS.strip() == "[literal]_":
                continue
            if re.search(_rgx, uS):  # check for tag
                utgS = self._tags(uS, tagL)
                self.restS += utgS.rstrip() + "\n"
                continue
            if typeS == "values":  # chk for values
                self.setcmdD["saveB"] = False
                if "=" in uS and uS.strip()[-2] == "||":  # value to file
                    uS = uS.replace("||", " ")
                    self.setcmdD["saveB"] = True
                if "=" in uS:  # assign value
                    uL = uS.split("|")
                    self._vassign(uL)
                    continue
            if typeS == "table":  # check for table
                if uS[0:2] == "||":
                    uL = uS[2:].split("|")
                    indxI = cmdL.index(uL[0].strip())
                    methL[indxI](uL)
                    continue
                else:
                    exec(uS)  # exec table code
                    continue
            if uS[0:2] == "||":  # check for cmd
                # print(f"{cmdL=}")
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                methL[indxI](uL)
                continue  # call any cmd

            self.rivtD.update(locals())
            if typeS != "table":  # skip table prnt
                self.restS += uS.rstrip() + "\n"

    def i_rst(self) -> tuple:
        """parse insert-string

        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings

        convert rivt-strings to reST strings

        Args:
        :param exportS (str): stores values that are written to file
        :param strL (list): calc rivt-strings
        folderD (dict): folder paths
        setcmdD (dict): command settings
        setsectD (dict): section settings
        rivtD (dict): global rivt dictionary

        """

        icmdL = ["text", "table", "image"]
        imethL = [
            self._itext,
            self._itable,
            self._iimage,
        ]

        self._parseRST("insert", icmdL, imethL, itagL)
        return self.restS, self.setsectD, self.setcmdD

    def v_rst(self) -> tuple:
        """parse value-string and set method

        Return:
        calcS (list): utf formatted calc-string (appended)
        setsectD (dict): section settings
        setcmdD (dict): command settings
        rivtD (list): calculation results
        exportS (list): value strings for export
        """

        locals().update(self.rivtD)
        vcmdL = ["config", "value", "data", "func", "text", "table", "image"]
        vmethL = [
            self._vconfig,
            self._vvalue,
            self._vdata,
            self._vfunc,
            self._itext,
            self._itable,
            self._iimage,
        ]

        self._parseRST("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.restS, self.setsectD, self.setcmdD, self.rivtD, self.exportS

    def t_rst(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation values
        """

        tcmdL = ["text", "table", "image"]
        tmethL = [self._itext, self._itable, self._iimage]

        self._parseUTF("table", tcmdL, tmethL, ttagL)

        return self.calcS, self.setsectD, self.setcmdD, self.rivtD
