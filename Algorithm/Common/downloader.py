import subprocess
import shutil
import os


# 给定子目录文件夹，从其中复制文件到当前运行的.cache文件夹目录下面
def download_data(sub_folder = r'PPG\ppg_emotion\example#1'):
    # 共享文件夹路径
    shared_folder = r'E:\Dataset'
    # 本地目标目录
    local_target_dir = os.path.join(os.getcwd(), '.cache')
    print("local target dir: ", local_target_dir)

    # 如果目标目录不存在，则创建它
    if not os.path.exists(local_target_dir):
        os.makedirs(local_target_dir)

    try:
        # 复制共享文件夹中的内容到本地目标目录
        shutil.copy(shared_folder, local_target_dir)
        print("文件复制完成！")
    except Exception as e:
        print("文件复制失败:", e)



# 给定子目录文件夹，从其中下载数据并缓存到本地的.cache文件夹目录下面
def download_data_remote(sub_folder = r'PPG\ppg_emotion\example#1'):
    # 远程共享文件夹信息
    remote_shared_folder = r'\\CHINAMI-9TV1I33\Dataset'
    remote_username = 'admin'
    remote_password = '123456'

    # 本地目标目录
    local_target_dir = os.path.join(os.getcwd(), '.cache')
    print("local target dir: ", local_target_dir)

    # 如果目标目录不存在，则创建它
    if not os.path.exists(local_target_dir):
        os.makedirs(local_target_dir)

    # 使用 net use 命令挂载远程共享文件夹
    net_use_command = f"net use Z: {remote_shared_folder} /user:{remote_username} {remote_password} /persistent:no"
    subprocess.run(net_use_command, shell=True)

    # 复制远程共享文件夹中的内容到本地目标目录
    try:
        shutil.copy('Z:', local_target_dir)
        print("文件复制完成！")
    except Exception as e:
        print("文件复制失败:", e)
    finally:
        # 卸载远程共享文件夹
        subprocess.run('net use Z: /delete', shell=True)



if __name__ == '__main__':
    sub_folder = r'PPG\ppg_emotion\example#1'
    download_data(sub_folder)




