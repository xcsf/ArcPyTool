### 1.更据使用的环境需要将CustomTransformations 文件夹下的文件复制到相应的位置
如：
**10.6**
C:\Users\Mr_Yin\AppData\Roaming\Esri\Desktop10.6\ArcToolbox\CustomTransformations
**ArcGIS pro**
C:\Users\Mr_Yin\AppData\Roaming\Esri\ArcGISPro\ArcToolbox\CustomTransformations

###  2.static.gdb
里面的要素表示 深圳独立 与 北京54中央经线114度高斯投影  互转的偏移量以及方向

### 3.54114tonewsz.txt 与 newszto54114.txt 为偏移起始坐标

###  4.由于深圳独立坐标更新  这里偏移数据存在两份 标有old的数据为老深圳独立坐标  新的数据使用肉眼纠偏。。。。  待更新~~~~

### 5. 其他的有很多实验数据，三个脚本干啥的看名字就懂了。

### 6. SZ坐标下RVT数据转84脚本目前需求不用暂时不管

### 7. 新加支持栅格数据集转换工具。

## 8. 不能修改文件目录结构，54114tonewsz.txt、newszto54114.txt、static.gdb

### 9.较表格中的深圳独立坐标  新的深圳独立坐标	小坐标X(南/北)-40m，大坐标Y(东/西)+34m

### 10.新加批量处理脚本  不过没完善 。。

