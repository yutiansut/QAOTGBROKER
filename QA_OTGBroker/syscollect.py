import sys
import ctypes
import os
import base64


def get_system_info():
    app_id = "SHINNY_TQ_1.0"

    system_info = ""

    try:

        l = ctypes.c_int(344)

        buf = ctypes.create_string_buffer(l.value)

        lib_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "ctpse")

        if sys.platform.startswith("win"):

            if ctypes.sizeof(ctypes.c_voidp) == 4:

                selib = ctypes.cdll.LoadLibrary(
                    os.path.join(lib_path, "WinDataCollect32.dll"))

                ret = getattr(selib, "?CTP_GetSystemInfo@@YAHPADAAH@Z")(
                    buf, ctypes.byref(l))

            else:

                selib = ctypes.cdll.LoadLibrary(
                    os.path.join(lib_path, "WinDataCollect64.dll"))

                ret = getattr(selib, "?CTP_GetSystemInfo@@YAHPEADAEAH@Z")(
                    buf, ctypes.byref(l))

        elif sys.platform.startswith("linux"):

            selib = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "LinuxDataCollect64.so"))

            ret = selib._Z17CTP_GetSystemInfoPcRi(buf, ctypes.byref(l))

        else:

            raise Exception("不支持该平台")

        if ret == 0:

            system_info = base64.b64encode(buf.raw[:l.value]).decode("utf-8")

        else:

            raise Exception("错误码: %d" % ret)

    except Exception as e:

        print(e)

    return app_id, system_info