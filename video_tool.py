# 读取视频的一些方法：1）ffmpeg工具；2）cv2.VideoCapture()方法；3）skvideo包 4）video2frame工具 https://github.com/jinyu121/video2frame

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
$ ffmpeg -i input.avi output.mp4    #可以将avi格式的视频转换为mp4格式的视频

音频提取
$ ffmpeg -i 222.mp4 -acodec aac -vn output.aac

视频提取
$ ffmpeg -i input.mp4 -vcodec copy -an output.mp4

视频剪切
$ ffmpeg -ss 00:00:15 -t 00:00:05 -i input.mp4 -vcodec copy -acodec copy output.mp4  
# 上述命令可以从00:00:15开始截取5s时常的视频， -ss 表示开始切割时间，-t 切割的时常

码率控制
码率控制对于在线视频比较重要。因为在线视频需要考虑其能提供的带宽。
那么，什么是码率？很简单： bitrate = file size / duration
比如一个文件20.8M，时长1分钟，那么，码率就是：
biterate = 20.8M bit/60s = 20.8*1024*1024*8 bit/60s= 2831Kbps
一般音频的码率只有固定几种，比如是128Kbps， 那么，video的就是
video biterate = 2831Kbps -128Kbps = 2703Kbps.

视频大小裁剪
$ ffmpeg -i input.mp4 -vf scale=960:540 output.mp4
# 将输入视频裁剪到960x540输出

抽帧
$ ffmpeg -i "*.mp4" -r 1 -q:v 2 -f image2 %d.jpeg
# -i 用来获取输入的文件   
# -r 设置每秒提取图片的帧数，-r 1的意思就是设置为每秒获取1帧；
# -q:v 2 提高抽取到的图片的质量的
# -f 强迫采用格式fmt 
# 上述命令执行结果是在当前目录下面就可以找到抽出来的图片了。

将图片序列合成视频
$ ffmpeg -f image2 -i pic-%03d.jpeg -vcodec xvid -r 30 -b:v 8000k test.mp4
#  -r 生成视频的帧， -b 码率 bit单位， -vcodec 编码格式
-----------------------------------------------------------------------------------------------------------------------------------

opencv 中的 VideoCapture类对视频进行读操作， VideoWrite类对视频进行写操作
VideoCapture()：支持读取本地视频文件（如.avi, .mp4等），也支持直接读取摄像机（电脑的视像头）

读取本地视频：
capture = cv2.VideoCaputer('test.avi') # 当参数为0时，代表读取摄像头数据
# 获取视频的属性
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) #总帧数
frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) # 视频的宽
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 高
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS) # fps

for i in range(frame_count):
  # 读取一帧图片，sucess表示是否读取成果， frame当前帧的数据
  success, frame = videoCapture.read()
#注意　VideoCapture会忽略掉重复的帧，而FFmpeg则会毫无问题的返回全部帧。因此在调用VideoCapture时实际得到的帧数会近似等于总帧数减去重复帧。
#的使用ffmpeg对这个视频抽帧可以得到300帧图片，而其中有大量连续重复的帧。这在整个数据集中也是很常见的。

---------------------------------------------------------------------------------------------------------------------------------
scikit-video工具

安装 $ sudo pip install sk-video
---------------------------------------------------------------------------
读视频：
import skvideo.io
import skvideo.datasets
import numpy as np 

# read video as a single ndarray
videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny())
print(videodata.shape)

# read video frame by frame
videogen = skvideo.io.vreader(skvideo.datasets.bigbuckbunny())
for frame in videogen:
    print(frame.shape)

# set keys and values for parameters in ffmpeg
inputparameters = {}
outputparameters = {}
reader = skvideo.io.FFmpegReader(skvideo.datasets.bigbuckbunny(),
                inputdict=inputparameters,
                outputdict=outputparameters)
# iterate through the frames
accumulation = 0
for frame in reader.nextFrame():
    # do something with the ndarray frame
    accumulation += np.sum(frame)

---------------------------------------------------------------------
写视频：
import skvideo.io
import skvideo.datasets
import numpy as np 

# write an ndarray to a video file
outputdata = np.random.random(size=(30,480,680,3)) * 255
outputdata = outputdata.astype(np.uint8)
skvideo.io.vwrite("outputvideo.mp4", outputdata)


# FFmpeg writer (报错)
outputdats = np.random.random(size=(5,480,680,3)) * 255
outputdata = outputdata.astype(np.uint8)
writer = skvideo.io.FFmpegWriter("outputvideoplus.mp4",(5,480,640,3))
for i in xrange(5):
    writer.writeFrame(outputdata[i,:,:,:])
writer.close()

-----------------------------------------------------------------------------
读取元数据（meta-data）
import skvideo.io
import skvideo.datasets
import json

metadata = skvideo.io.ffprobe(skvideo.datasets.bigbuckbunny())
print(metadata.keys())
print(json.dumps(metadata['video'], indent=4))

--------------------------------------------------------------------------------
运动：
import skvideo.io 
import skvideo.motion
import skvideo.datasets

videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny(),num_frames=5)


motion = skvideo.motion.blockMotion(videodata)

print(videodata.shape)
print(motion.shape)

# compensate the video
compensate = skvideo.motion.blockComp(videodata, motion)

# write
skvideo.io.vwrite("compensate.mp4", compensate)

-----------------------------------------------------------------------
测量：
import skvideo.io 
import skvideo.motion
import skvideo.datasets
import skvideo.measure

# compute vectors from bigbuckbunny
videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny(),num_frames=5,as_grey=True)
# videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny())
# skvideo.io.vwrite("origin.mp4", videodata)

motion = skvideo.motion.blockMotion(videodata)

print(videodata.shape)
print(motion.shape)

# compensate the video
compensate = skvideo.motion.blockComp(videodata, motion)

# write
skvideo.io.vwrite("compensate.mp4", compensate)

print(skvideo.measure.ssim(videodata,compensate))
print(skvideo.measure.psnr(videodata,compensate))
print(skvideo.measure.mse(videodata,compensate))

---------------------------------------------------------------------
读写图片
import skvideo.io 

# a frame from the bigbuckbunny sequence
vid = skvideo.io.vread('/home/shuai/python_test/output.png')
T, M, N, C = vid.shape

print("Number of frames: %d" % (T,))
print("Number of rows: %d" % (M,))
print("Number of cols: %d" % (N,))
print("Number of channels: %d" % (C,))

# upsacle by a factor of 2
vid = skvideo.io.vread('/home/shuai/python_test/output.png',
                        outputdict={
                            "-sws_flags":"bilinear",
                            "-s":"2560x1440"
                        })
T, M, N, C = vid.shape

print("Number of frames: %d" % (T,))
print("Number of rows: %d" % (M,))
print("Number of cols: %d" % (N,))
print("Number of channels: %d" % (C,))

skvideo.io.vwrite("outputplus.png", vid)
