# Yingshaoxo Computer

This has no English version because for some words, in my mind, only chinese can be used to do the expression.

If you want a english version, you can look for 'yingshaoxo_linux' folder, where I also said something about computer hardware.


## 基于墨水屏的超省电平板电脑设计

1. 基于x86的surface平板电脑，可接键盘。板载一个界面美化版的xp系统。
2. 背壳用软塑料做，可像卷饼一样拉开，露出墨水屏。不拉开时两边有磁吸点，不会自己打开。
3. 墨水屏在使用时，原x86系统只启动1核且降低运算频率，原LED屏幕断电。
4. 至少可以用3天，因为墨水屏幕几乎不用电。(这个屏幕看书也有好处，没有辐射、没有高光。这个屏幕操作黑白terminal/shell也有好处。)
5. 把电池改为几个5v电池的组合，需要12v时用串联的电，平时充电用并联5v。完美实现5v电源适配器给笔记本电脑充电。


## 基于单片机的超长待机笔记本电脑设计

1. 基于传统x86/i32 Linux笔记本电脑，无GPU，wifi模块可以硬断电，减少耗电设备。
2. 顶部屏幕有一个480x320的凹陷。用一块单片机彩色屏幕把它填满。
3. 正常工作时，单片机彩色屏幕和原笔记本屏幕联动。看起来就像正常完整的彩色屏幕，显示完整的图像。只是有一个不明显的480x320黑边线。
4. 敲命令行“power_save_mode”进入超长待机模式后，主_x86_Linux系统 进入 hibernate，把当前运行系统的内存放进硬盘，断电，主屏幕断电。小单片机彩屏与某内置单片机开始工作，继续支撑terminal shell。
5. 小单片机彩色屏幕现在是一个小terminal，可操作原x86系统的硬盘存储，比如编辑文本。该单片机暂时定为 micropython board。
6. 该笔记本的待机时长取决于单片机+小屏幕的待机时长。一般为1周，因为电池为1.2万毫安的笔记本电脑，且电压只有5v。中途当你想切换回大系统，你只需要运行命令行"normal_mode"。大的linux系统会在3秒后恢复成你上次休眠的状态，连之前使用过的软件都是被打开的状态。你可以接着工作。
7. 如果还是耗电，可以把小屏幕甚至大屏幕替换为 墨水屏，这种屏幕一旦图像被更改，就不需要更多的电力去维持屏幕显示。
8. 把电池改为几个5v电池的组合，需要12v时用串联的电，平时充电用并联5v。完美实现5v电源适配器给笔记本电脑充电。

