# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# arankUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by CoderXKrishna@Github.

# This file is part of: https://github.com/CoderXKrishna/arankuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/CoderXKrishna/arankuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# special credits: Ported from @UniBorg

from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from ..core.logger import logging

LOGS = logging.getLogger(__name__)


async def is_admin(arankub, chat_id, userid):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        req_jo = await arankub.get_permissions(chat_id, userid)
        chat_participant = req_jo.participant
        if isinstance(
            chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
        ):
            return True
    except Exception as e:
        LOGS.info(str(e))
        return False
    else:
        return False
