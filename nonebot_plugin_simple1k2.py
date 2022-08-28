from nonebot.plugin.on import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message

helpText = "请输入：一穿二 剩余秒数 BOSS血量 目标补偿（非必需）\n如：“一穿二 34 2000”或“一穿二 34 2000 56”"
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
async def feedback(command_arg: Message = CommandArg()):
    command_arg_list = command_arg.extract_plain_text().split()
    command_arg_length = len(command_arg_list)
    if command_arg_length == 0:
        await simple_1k2_matcher.finish(helpText)
    if not 2 <= command_arg_length <= 3:
        await simple_1k2_matcher.finish(helpText + "\n错误0")
    try:
        c1 = float(command_arg_list[0])
        c2 = float(command_arg_list[1])
    except:
        await simple_1k2_matcher.finish(helpText + "\n错误1")
    if c1 <= 0 or c2 <= 0 or c1 >= 90:
        await simple_1k2_matcher.finish("输入数字错误")
    elif c1 >= 35:
        await simple_1k2_matcher.finish("无需填补即可一穿二")
    if command_arg_length == 2:
        result = calc(c1, c2)
        needs = c2 - result
    elif command_arg_length == 3:
        try:
            c3 = float(command_arg_list[2])
        except:
            await simple_1k2_matcher.finish(helpText + "\n错误2")
        if not (c3 >= (c1 + 20) and c3 <= 90):
            await simple_1k2_matcher.finish("目标补偿时间错误，必须不小于剩余时间+20s且不大于90s")
        result = calc(c1, c2, c3)
        needs = c2 - result
    reply = "若要按需求完成一穿二，应至少填{:.2f}伤害，使当前BOSS血量降至{:.2f}以下。".format(needs, result)
    await simple_1k2_matcher.finish(reply)
