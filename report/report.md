# <center>交通灯识别  实验报告

薛皓阳 2020010647

[TOC]

## 1. 使用预训练好的 YOLOv5 模型在交通灯检测测试集上得到测试结果。

### (1) 使用模型检测交通灯图像

待检测图像（40402号图像）：

<img src="\images\40402_original.png" alt="original" style="zoom:50%;" />

检测结果：

<img src="\images\40402_detected.png" alt="original" style="zoom:50%;" />

### (2) 使用给出标注生成图像标签

#### a) 生成标注

代码文件：`CreateLabels&CropImages.py`

文件说明：考虑到需要遍历每一张图片的标注，本文件实现了函数`CreateLabelsAndCropImages()`实现三个功能：1. 基本功能：可以将`test.json`中的标注结果输出为标注文件，保存至`/labels/`文件夹下（图像名称.txt），若剪裁则左半部分图像名后接‘_l’，右半部分图像名后接‘\_r’。2. 可选功能：`x_cropping`选择是否将图像从中间一分为二，具体分析见 *2. 优化检测模型*。3. 可选功能：在上一功能的基础上可选`y_cropping`选择是否选取图像中央部分，具体分析见 *2. 优化检测模型*。

函数输入：

```python
`jsonPath`:     test.json路径
`label_dest`:   label目标位置
`img_dest`:     剪裁后图片目标位置
`img_src`:      待处理图像位置
`w`:            图像宽度
`h`:            图像高度
`x_cropping`:   x方向是否剪裁
`y_cropping`:   y方向是否剪裁
```

运行结果：在目标位置生成相应文件，可以使用`val.py`进行验证。

#### b) 结果指标

考虑到仅测试在交通灯类上的准确度，因此`val.py`输出的 mAP50 和 mAP50-95 均为交通信号灯本类的结果，则可以将 mAP50 和 mAP50-95 作为检测结果的定量指标。

## 2. 优化检测模型

### (1) 调节参数并对图像预处理，使整体交通灯检测指标提升

#### a) 调节参数

经过调试发现对结果影响最大的参数是输入网络的图像大小（imgsz），不同imgsz对结果的影响如下：

| 参数                 | mAP50  | mAP50-95 |
| -------------------- | ------ | -------- |
| imgsz = 640 默认参数 | 0.0828 | 0.0211   |
| imgsz = 1920         | 0.339  | 0.131    |

可以看到提升imgsz可以大幅度提高mAP的结果。

#### b) 预处理

##### i) 图像增强

使用文件：`Color_Enhancement.py`

调用PIL库的`ImageEnhancement`类对图像做增强，图像锐度调整为2，对比度调整为0.5，imgsz=640时验证结果优于原图（其他增强方式均更差）对比结果如下：

| 图像类型   | imgsz | mAP50  | mAP50-85 |
| ---------- | ----- | ------ | -------- |
| 原始图像   | 640   | 0.0828 | 0.0211   |
| 图像增强后 | 640   | 0.0887 | 0.0225   |
| 原始图像   | 1920  | 0.339  | 0.131    |
| 图像增强后 | 1920  | 0.325  | 0.117    |

在 imgsz=1920 时，图像增强效果不如未做图像增强的结果，因此放弃图像增强。

##### ii) 图像剪裁

###### 理论分析

考虑先验知识：交通灯一般出现在道路两侧，且高度一般位于图像中间。基于此先验可以将图像中交通灯几乎不会出现的区域剪裁掉，以提高检测目标在图像中的占比。

使用文件`json2mat.py`将`test.json`的内容导出至`Project/matlab_process/positions.mat`，在`analyze.m`中对标注位置分析。

对`x_max、x_min、y_max、y_min`做直方图统计出现频次，结果如下：

![feature_analyzation](\images\feature_analyzation.png)

- 可以发现在x方向信号灯标注框不会出现在图像正中间（640处），且y方向标注框集中在320附近。
- 经过计算，`y_max`和`y_min`的所有数据中，98.21%的数据出现在$320\pm150$个像素的范围内。

因此可以将原始图像以640为界切分为左右两图，同时y方向抛弃470像素以上、170像素以下的部分。

具体操作：在`CreateLabels&CropImages.py`文件中检查标注框的位置，根据左右划分为左图和右图，同时对原图像做左右和上下切分（`x_cropping`和`y_cropping`），如果某半张图中没有标注框则忽略这半张图（不保存，不生成标注文件）。切分结果如下：

- 原图：
  - <img src="\images\35376.png" alt="35376" style="zoom:30%;" />
  
- `x_cropping`切分后：

  - 左：<img src="\images\x_35376_l.png" alt="35376_l" style="zoom:30%;" />	右：<img src="\images\x_35376_r.png" alt="35376_r" style="zoom:30%;" />

- `xy_cropping`切分后：
  
  - 左：<img src="\images\xy_35376_l.png" alt="35376_l" style="zoom:30%;" />	右：<img src="\images\xy_35376_r.png" alt="35376_r" style="zoom:30%;" />
  
    

可以观察到一张图的两个信号灯被分到了一左一右两张图中。在此情况下，验证结果可能会表现得更好。

###### 验证结果

对x、y方向剪裁后的图像（图像集为`xy_cropped`）做验证，与原始结果和仅做x方向剪裁的结果对比如下（imgsz=1920）：

| 剪裁类型      | mAP50 | mAP50-95 |
| ------------- | ----- | -------- |
| 无            | 0.339 | 0.131    |
| `x_cropping`  | 0.428 | 0.198    |
| `xy_cropping` | 0.410 | 0.191    |

可以看到`xy_cropping`的结果略低于`x_cropping`，可能的解释为：`x_cropping`之后图像为正方形（宽长比为0.889），送入网络经过拉伸的失真较小，更容易识别；而`xy_cropping`之后的图像由于丢弃了上下两块较大的区域，相较于正方形偏离度过大（宽长比为0.468），送入网络后经过较大的拉伸，产生较大的失真，可能使识别更不准确。

## 3. 实验总结

经过测试，将原始图像且分为左右两张图，不做图像增强，imgsz=1920时mAP50最大，可以达到0.428，相对于默认参数直接验证的结果（mAP50=0.0828）有较大的提升。

在此次实验中我针对yolov5的输入做了相应的预处理，统计分析了交通信号灯的出现范围，测试了多种预处理方法，经过比较得出了相对的局部最优解。我更加了解了yolo内部的实现方式，尝试了将人类的先验知识加入到图像处理的工作之中，巩固了所学到的知识，收获颇丰。

## 4. 文件清单

*仅展示原创部分*

```
Project
├─ dataset_test_rgb_small
│  ├─ Color_Enhancement.py		    图像增强
│  ├─ CreateLabels&CropImages.py	生成标签及图像剪裁
│  ├─ json2mat.py				   将test.json中的内容导出至matlab_process/positions.mat
│  ├─ White_balance.py            	对图像做白平衡
│  ├─ rgb
│  └─ image_sets
│  	  ├─ cropped_enhanced
│  	  ├─ enhanced
│  	  ├─ original
│  	  ├─ white_balanced
│  	  ├─ xy_cropped
│  	  └─ x_cropped
├─ matlab_process
│ 	├─ analyze.m                  标签位置分析
│ 	└─ positions.mat              test.json内容导出结果
├─ report
├─ results
│  	└─ test_log.md                测试日志
└─ yolov5-master
	└─ data
		└─ project.yaml
```

注：如何切换不同的验证集：在Project/yolov5-master/data/project.yaml文件中将`val: image_sets/`一行改为需要验证的图像集，例如：`val: image_sets/enhanced`。

