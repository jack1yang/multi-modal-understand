# 读取视频的一些方法：1）ffmpeg工具；2）cv2.VideoCapture()方法；3）skvideo包

# 首先介绍ffmpeg工具和一些常用命令，  参考https://www.jianshu.com/p/2c00a1a59af1
# 主要参数: 
-i 设定输入流
-f 设置输出格式
-ss 开始时间
# 视频参数
-b 设定视频流量(码率)，默认为200Kbit/s 
-r 设定帧速率，默认为25 
-s 设定画面的宽与高 
-aspect 设定画面的比例 
-vn 不处理视频 
-vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器 

#音频参数
-ar 设定采样率 
-ac 设定声音的Channel数 
-acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器 
-an 不处理音频

常用功能：
视频格式转换
>>> ffmpeg -i input.avi output.mp4    #可以将avi格式的视频转换为mp4格式的视频

音频提取
>>> ffmpeg -i 222.mp4 -acodec aac -vn output.aac

视频提取
>>> ffmpeg -i input.mp4 -vcodec copy -an output.mp4

视频剪切
>>> ffmpeg -ss 00:00:15 -t 00:00:05 -i input.mp4 -vcodec copy -acodec copy output.mp4  
# 上述命令可以从00:00:15开始截取5s时常的视频， -ss 表示开始切割时间，-t 切割的时常

码率控制
码率控制对于在线视频比较重要。因为在线视频需要考虑其能提供的带宽。
那么，什么是码率？很简单： bitrate = file size / duration
比如一个文件20.8M，时长1分钟，那么，码率就是：
biterate = 20.8M bit/60s = 20.8*1024*1024*8 bit/60s= 2831Kbps
一般音频的码率只有固定几种，比如是128Kbps， 那么，video的就是
video biterate = 2831Kbps -128Kbps = 2703Kbps.

视频大小裁剪
>>> ffmpeg -i input.mp4 -vf scale=960:540 output.mp4
# 将输入视频裁剪到960x540输出

抽帧
>>> ffmpeg -i "*.mp4" -r 1 -q:v 2 -f image2 %d.jpeg
# -i 用来获取输入的文件   
# -r 设置每秒提取图片的帧数，-r 1的意思就是设置为每秒获取1帧；
# -q:v 2 提高抽取到的图片的质量的
# -f 强迫采用格式fmt 
# 上述命令执行结果是在当前目录下面就可以找到抽出来的图片了。
