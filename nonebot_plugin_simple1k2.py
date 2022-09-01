from nonebot.plugin.on import on_command
from nonebot.plugin.load import require
from nonebot.params import Depends
from typing import List

require("nonebot_plugin_kyaruutils")
from .nonebot_plugin_kyaruutils import ArgTools  # type:ignore

simple_1k2_matcher = on_command("一穿二")


def calc(x: float, y: float, *args: float) -> float:
    """
    PCR补偿进位采用进一法
    补偿时间 = 固定补偿（国服目前为20s）+（90-（BOSS当前血量/实际造成伤害（最高为当前血量））*造成伤害的时间）
    """
    if len(args) == 0:
        return float((y / (90 - x)) * (20 + x + 1))
    else:
        return float((y / (90 - x)) * (110 - args[0] + 1))


@simple_1k2_matcher.handle()
@ArgTools.filter_decorator(count=[2, 3], param_desp=["剩余时间", "BOSS血量", "期望时间"])
async def feedback(command_arg_list: List[float] = Depends(ArgTools.extract_list(proc_list=[float]))):
    command_arg_length = len(command_arg_list)
    c1 = command_arg_list[0]
    c2 = command_arg_list[1]
    if c1 <= 0 or c2 <= 0 or c1 >= 90:
        await simple_1k2_matcher.finish("参数错误：超出范围")
    if c1 >= 35:
        await simple_1k2_matcher.finish("无需填补即可一穿二")
    if command_arg_length == 2:
        result = calc(c1, c2)
        needs = c2 - result
    else:
        c3 = command_arg_list[2]
        if not (c3 >= (c1 + 20) and c3 <= 90):
            await simple_1k2_matcher.finish("目标补偿时间错误，必须不小于剩余时间+20s且不大于90s")
        result = calc(c1, c2, c3)
        needs = c2 - result
    reply = "至少需填补%.2f伤害\n使当前BOSS血量降至%.2f以下" % (needs, result)
    await simple_1k2_matcher.finish(reply)
