# Mouse-clicker

## 项目简介
Mouse-clicker 是一个简单的鼠标点击工具，用于自动化鼠标点击操作。

## 功能
- 支持单次点击和连续点击模式
- 可自定义点击间隔时间
- 支持记录多次点击的坐标，记录的坐标可以保存为文件，也可以从文件中读取坐标进行点击回放

### windows下图像界面
![鼠标点击器.jpg](doc/%E9%BC%A0%E6%A0%87%E7%82%B9%E5%87%BB%E5%99%A8.jpg)

## 安装步骤
1. 确保您的系统已安装 Python 3.x
2. 克隆本项目到本地：
   ```bash
   git clone https://github.com/song-liang/Mouse-clicker.git
   ```
3. 进入项目目录：
   ```bash
   cd Mouse-clicker
   ```
4. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法
1. 运行程序：
   ```bash
   python mouse-clicker.py
   ```
2. 根据提示选择点击模式和参数
![鼠标点击器.jpg](doc/%E9%BC%A0%E6%A0%87%E7%82%B9%E5%87%BB%E5%99%A8.jpg)


## windows下打包成可只执行文件
1. 安装 nuitka(PyInstaller打包更简单快速，但是杀毒软件容易报毒，Nuitka打包出来的文件体积更小，运行速度更快)
```
pip install nuitka
```
2. 打包
```
python.exe -m nuitka --standalone --enable-plugin=tk-inter --windows-disable-console --windows-icon-from-ico=doc/mouse-clicker..ico mouse-clicker.py
```

3. 运行
打包结束后的可执行文件在dist目录下，运行即可
mouse-clicker.dist\mouse-clicker.exe



