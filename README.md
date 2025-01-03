# Jacob_Course_Selector

- ### Summary

  This is project is created by a Year-3 student majoring STAT program use for UIC's MIS course selection. It is code by Python3 along with modules: request, selenium, threading, etc. Kindly remind that this is only for study purpose and **author will not response for your consequence for using this script.**

- ### Usage

  1. Please make sure the installation of Python3 and the Chrome browser then use following command to install requirement in command line.

     ```cmd
     pip install -r requirements.txt
     ```

  2. Under the same directory, execute following command to run the script.

     ```cmd
     python main.py
     ```

  3. Follow the instruction, if you run the script for the first time, you have to manually configurate `config.ini` file.

     ![image-20250104043044744](https://github.com/KOISHI-KAWAI/Jacob_Course_Selector/blob/main/example.png)

     Input course name (section) you would like to pick from red rectangle (No space), and fill the configuration file like this. (You only need to worry about the course name under the each row of typeName, electiveTypeId).

     ```ini
     # 登录页面配置
     login_URL = https://mis.uic.edu.cn/mis/login.jsp    
     elective_URL = https://mis.uic.edu.cn/mis/student/es/elective.do
     detail_URL = https://mis.uic.edu.cn/mis/student/es/eleDetail.do
     select_URL = https://mis.uic.edu.cn/mis/student/es/select.do
     
     # 选课配置 (格式如下)
     
     # typeName1, electiveTypeId1:
     # sectionName1
     # sectionName2
     # ... 
     #
     # typeName2, electiveTypeId2:
     # sectionName1
     # sectionName2
     # ...
     #
     #...
     
     # 从这里开始填写
     GE2021(Level 2) - GTCU/GTSC/GTSU, 2c9070189384f1440193b9ef177755d1:
     Appreciation of Applied Mathematics (1001)
     
     Major Elective, 2c9070189384f1440193b9ef17835616:
     Experimental Design (1001)
     
     FE, 2c9070189384f1440193b9ef177755cc:
     Business and Society (1001)
     ```

  4. After editing configuration file, following the instruction and give command when permit to select course. The whole process should be like this.

     ```ini
     [+] 读取配置文件，请保证config.ini文件在同一目录下
     [+] 打开选课界面，请手动登录
     [+] 成功登录选课系统
     [+] 是否首次运行脚本？Y/N :Y
     [!] 请打开config.ini配置文件，填写选课信息
     完成后按任意键继续...
     [+] 获取选课ID中, 请勿关闭浏览器
         [-] 找到课程 <Appreciation of Applied Mathematics (1001)> ID: 2c9070d993f17ea301941a50f31577aa
         [-] 找到课程 <Experimental Design (1001)> ID: 2c9070d993f17ea301941a4dc5e60656
         [-] 找到课程 <Business and Society (1001)> ID: 2c9070d993f17ea301941a60fce623cc
     [+] 选课ID获取完成
     [+] 请在选课开始后输入start开始选课: start
     [+] 总共启动 3 个选课线程
         [-] 正在选课 ID: 2c9070d993f17ea301941a50f31577aa
         [-] 正在选课 ID: 2c9070d993f17ea301941a4dc5e60656
         [-] 正在选课 ID: 2c9070d993f17ea301941a60fce623cc
         [-] 选课成功 ID: 2c9070d993f17ea301941a60fce623cc
         [-] 选课成功 ID: 2c9070d993f17ea301941a4dc5e60656
         [-] 选课成功 ID: 2c9070d993f17ea301941a50f31577aa
     ```

     

