# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# arankUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by CoderXKrishna@Github.

# This file is part of: https://github.com/CoderXKrishna/arankuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/CoderXKrishna/arankuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import io
import os
import shutil
import time
from pathlib import Path

from userbot import arankub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _arankutils, _format
from . import humanbytes

plugin_category = "tools"


@arankub.arank_cmd(
    pattern="ls(?:\s|$)([\s\S]*)",
    command=("ls", plugin_category),
    info={
        "header": "To list all files and folders.",
        "description": "Will show all files and folders if no path is given or folder path is given else will show file details(if file path os given).",
        "usage": "{tr}ls <path>",
        "examples": "{tr}ls userbot",
    },
)
async def ls(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    "To list all files and folders."
    arank = "".join(event.text.split(maxsplit=1)[1:])
    path = arank or os.getcwd()
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"there is no such directory or file with the name `{arank}` check again",
        )
        return
    path = Path(arank) if arank else os.getcwd()
    if os.path.isdir(path):
        if arank:
            msg = f"Folders and Files in `{path}` :\n"
        else:
            msg = "Folders and Files in Current Directory :\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            arankpath = os.path.join(path, contents)
            if not os.path.isdir(arankpath):
                size = os.stat(arankpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎵`{contents}`\n"
                if str(contents).endswith((".opus")):
                    files += f"🎙`{contents}`\n"
                elif str(contents).endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += f"🎞`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"🗜`{contents}`\n"
                elif str(contents).endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")
                ):
                    files += f"🖼`{contents}`\n"
                else:
                    files += f"📄`{contents}`\n"
            else:
                folders += f"📁`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
    else:
        size = os.stat(path).st_size
        msg = "The details of given file :\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        if str(path).endswith((".opus")):
            mode = "🎙"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "🗜"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🖼"
        else:
            mode = "📄"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Loarankion :** `{path}`\n"
        msg += f"**icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await event.delete()
    else:
        await edit_or_reply(event, msg)


@arankub.arank_cmd(
    pattern="rem(?:\s|$)([\s\S]*)",
    command=("rem", plugin_category),
    info={
        "header": "To delete a file or folder from the server",
        "usage": "{tr}rem <path>",
        "examples": "{tr}rem Dockerfile",
    },
)
async def rem(event):
    "To delete a file or folder."
    arank = event.pattern_match.group(1)
    if arank:
        path = Path(arank)
    else:
        await edit_or_reply(event, "what should i delete")
        return
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"there is no such directory or file with the name `{arank}` check again",
        )
        return
    arankcmd = f"rm -rf '{path}'"
    if os.path.isdir(path):
        await _arankutils.runcmd(arankcmd)
        await edit_or_reply(event, f"successfully removed `{path}` directory")
    else:
        await _arankutils.runcmd(arankcmd)
        await edit_or_reply(event, f"successfully removed `{path}` file")


@arankub.arank_cmd(
    pattern="mkdir(?:\s|$)([\s\S]*)",
    command=("mkdir", plugin_category),
    info={
        "header": "To create a new directory.",
        "usage": "{tr}mkdir <topic>",
        "examples": "{tr}mkdir arank",
    },
)
async def make_dir(event):
    "To create a new directory."
    pwd = os.getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(
            event,
            "What should i create ?",
            parse_mode=_format.parse_pre,
        )
    original = os.path.join(pwd, input_str.strip())
    if os.path.exists(original):
        await edit_delete(
            event,
            f"Already a directory named {original} exists",
        )
        return
    mone = await edit_or_reply(
        event, "creating the directory ...", parse_mode=_format.parse_pre
    )
    await asyncio.sleep(2)
    try:
        await _arankutils.runcmd(f"mkdir {original}")
        await mone.edit(f"Successfully created the directory `{original}`")
    except Exception as e:
        await edit_delete(mone, str(e), parse_mode=_format.parse_pre)


@arankub.arank_cmd(
    pattern="cpto(?:\s|$)([\s\S]*)",
    command=("cpto", plugin_category),
    info={
        "header": "To copy a file from one directory to other directory",
        "usage": "{tr}cpto from ; to destination",
        "examples": "{tr}cpto sample_config.py ; downloads",
    },
)
async def copy(event):
    "To copy a file from one directory to other directory"
    pwd = os.getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(
            event,
            "What and where should i move the file/folder.",
            parse_mode=_format.parse_pre,
        )
    loc = input_str.split(";")
    if len(loc) != 2:
        return await edit_delete(
            event,
            "use proper syntax .cpto from ; to destination",
            parse_mode=_format.parse_pre,
        )
    original = os.path.join(pwd, loc[0].strip())
    loarankion = os.path.join(pwd, loc[1].strip())

    if not os.path.exists(original):
        await edit_delete(
            event,
            f"there is no such directory or file with the name `{original}` check again",
        )
        return
    mone = await edit_or_reply(
        event, "copying the file ...", parse_mode=_format.parse_pre
    )
    await asyncio.sleep(2)
    try:
        await _arankutils.runcmd(f"cp -r {original} {loarankion}")
        await mone.edit(f"Successfully copied the `{original}` to `{loarankion}`")
    except Exception as e:
        await edit_delete(mone, str(e), parse_mode=_format.parse_pre)


@arankub.arank_cmd(
    pattern="mvto(?:\s|$)([\s\S]*)",
    command=("mvto", plugin_category),
    info={
        "header": "To move a file from one directory to other directory.",
        "usage": "{tr}mvto frompath ; topath",
        "examples": "{tr}mvto stringsession.py ; downloads",
    },
)
async def move(event):
    "To move a file from one directory to other directory"
    pwd = os.getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(
            event,
            "What and where should i move the file/folder.",
            parse_mode=_format.parse_pre,
        )
    loc = input_str.split(";")
    if len(loc) != 2:
        return await edit_delete(
            event,
            "use proper syntax .mvto from ; to destination",
            parse_mode=_format.parse_pre,
        )
    original = os.path.join(pwd, loc[0].strip())
    loarankion = os.path.join(pwd, loc[1].strip())

    if not os.path.exists(original):
        return await edit_delete(
            event,
            f"there is no such directory or file with the name `{original}` check again",
        )
    mone = await edit_or_reply(
        event, "Moving the file ...", parse_mode=_format.parse_pre
    )
    await asyncio.sleep(2)
    try:
        shutil.move(original, loarankion)
        await mone.edit(f"Successfully moved the `{original}` to `{loarankion}`")
    except Exception as e:
        await edit_delete(mone, str(e), parse_mode=_format.parse_pre)
