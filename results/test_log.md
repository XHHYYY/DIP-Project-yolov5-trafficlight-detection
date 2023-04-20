# 测试日志
1. 原始数据集上直接验证，默认参数：imgsz = 640，未裁剪，数据集：original/images测试结果：

    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        200        195      0.168      0.222     0.0828     0.0211

2. 对原始数据集做白平衡，默认参数，未裁剪，数据集：white_balanced/images测试结果：
   
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        200        195       0.21      0.231     0.0763     0.0169

3. 对原始图像做图像增强，参数为：锐度2.0，对比度0.5，运行结果：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        200        195      0.215      0.164     0.0887     0.0225

4. 将增强后的图像且分为左右两部分测试，结果如下：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        175        195       0.34      0.297      0.182      0.057

5. 将原始图像直接切分测试，结果如下：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        175        195       0.37      0.349      0.209     0.0696

6. 原始图像切分，imgsz = 1920，结果如下：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        175        195      0.424      0.554      0.428      0.198

7. 原始图像切分，imgsz = 2560，结果如下：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        175        195      0.355      0.482      0.346      0.166

      反而更差了

      接下来的尝试：数据分析交通灯的位置特征（MATLAB），做进一步剪裁

8. 原始图像xy_crop，imgsz=1920：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        172        191      0.442      0.515       0.41      0.191
      
9.  原始图像x_crop,  imgsz=1920：
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        175        195      0.424      0.554      0.428      0.198

10. 原始图像，imgsz = 1920
    Class     Images  Instances          P          R      mAP50   mAP50-95
      all        200        195      0.414      0.467      0.339      0.131