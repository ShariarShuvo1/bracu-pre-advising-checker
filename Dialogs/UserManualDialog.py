from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout

from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE


class UserManualDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setWindowTitle(f"User Manual")
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.webview = QWebEngineView()

        html_content = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>User Manual</title>
              <style>
                body {
                  font-family: Arial, sans-serif;
                  background-color: #f2f2f2;
                  color: #333;
                  margin: 0;
                  padding: 0;
                }
                .container {
                  max-width: 800px;
                  margin: 20px auto;
                  background-color: #fff;
                  padding: 20px;
                  border-radius: 8px;
                  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                  color: #333;
                  text-align: center;
                }
                .section {
                  margin-bottom: 20px;
                }
                .section-title {
                  background-color: #007bff;
                  color: #fff;
                  padding: 10px;
                  border-radius: 4px 4px 0 0;
                }
                .data {
                  padding: 10px;
                  border: 1px solid #ccc;
                  border-top: none;
                  border-radius: 0 0 4px 4px;
                }
                .keyword {
                  font-weight: bold;
                  color: #007bff;
                }
              </style>
            </head>
            <body>
              <div class="container">
                <h1>User Manual</h1>
            
                <!-- Explanation Section -->
                <div class="section">
                  <div class="section-title">Explanation of Keywords</div>
                  <div class="data">
                    <p><span class="keyword">s:</span> Represents a section. To define a section, use <code>s=section_name</code>.</p>
                    <p><span class="keyword">c:</span> Stands for course code. You can specify the course code using <code>c=course_code</code>.</p>
                    <p><span class="keyword">i:</span> Indicates the instructor of the course. To include the instructor's name, use <code>i=instructor_name</code>.</p>
                    <p><span class="keyword">p:</span> Denotes the program related to the course. Specify the program using <code>p=program_name</code>.</p>
                    <p><span class="keyword">f:</span> Represents the faculty associated with the course. Include the faculty name using <code>f=faculty_name</code>.</p>
                    <p><span class="keyword">in:</span> Stands for instructor name. Include the instructor's name using <code>in=instructor_name</code>.</p>
                    <p><span class="keyword">ct:</span> Represents the course title. Specify the course title using <code>ct=course_title</code>.</p>
                    <p><span class="keyword">ts:</span> Indicates the total number of seats greater than a specified value. Specify the value using <code>ts=number</code>.</p>
                    <p><span class="keyword">sb:</span> Represents the number of seats booked greater than a specified value. Specify the value using <code>sb=number</code>.</p>
                    <p><span class="keyword">sr:</span> Indicates the number of seats remaining greater than a specified value. Specify the value using <code>sr=number</code>.</p>
                    <p><span class="keyword">e:</span> Denotes the exam date. Include the exam date using <code>e=exam_date</code>.</p>
                    <p><span class="keyword">ed:</span> Represents the exam day. Specify the exam day using <code>ed=exam_day</code>.</p>
                    <p><span class="keyword">es:</span> Indicates the exam start time. Specify the start time using <code>es=start_time</code>.</p>
                    <p><span class="keyword">ee:</span> Denotes the exam end time. Specify the end time using <code>ee=end_time</code>.</p>
                    <p><span class="keyword">c1:</span> Represents class 1 day. Use this keyword for specifying details related to class 1.</p>
                    <p><span class="keyword">c2:</span> Represents class 2 day. Use this keyword for specifying details related to class 2.</p>
                    <p><span class="keyword">l1:</span> Represents lab 1 day. Use this keyword for specifying details related to lab 1.</p>
                    <p><span class="keyword">l2:</span> Represents lab 2 day. Use this keyword for specifying details related to lab 2.</p>
                    <p>Here are some more keywords:</p>
                    <ul>
                      <li><span class="keyword">c1s:</span> Class 1 start time. Use <code>c1s=start_time</code>.</li>
                      <li><span class="keyword">c1e:</span> Class 1 end time. Use <code>c1e=end_time</code>.</li>
                      <li><span class="keyword">c1sr:</span> Class 1 start from. Use <code>c1sr=start_time</code>.</li>
                      <li><span class="keyword">c1er:</span> Class 1 end till. Use <code>c1er=end_time</code>.</li>
                      <li><span class="keyword">c2s:</span> Class 2 start time. Use <code>c2s=start_time</code>.</li>
                      <li><span class="keyword">c2e:</span> Class 2 end time. Use <code>c2e=end_time</code>.</li>
                      <li><span class="keyword">c2sr:</span> Class 2 start from. Use <code>c2sr=start_time</code>.</li>
                      <li><span class="keyword">c2er:</span> Class 2 end till. Use <code>c2er=end_time</code>.</li>
                      <li><span class="keyword">l1s:</span> Lab 1 start time. Use <code>l1s=start_time</code>.</li>
                      <li><span class="keyword">l1e:</span> Lab 1 end time. Use <code>l1e=end_time</code>.</li>
                      <li><span class="keyword">l1sr:</span> Lab 1 start from. Use <code>l1sr=start_time</code>.</li>
                      <li><span class="keyword">l1er:</span> Lab 1 end till. Use <code>l1er=end_time</code>.</li>
                      <li><span class="keyword">l2s:</span> Lab 2 start time. Use <code>l2s=start_time</code>.</li>
                      <li><span class="keyword">l2e:</span> Lab 2 end time. Use <code>l2e=end_time</code>.</li>
                      <li><span class="keyword">l2sr:</span> Lab 2 start from. Use <code>l2sr=start_time</code>.</li>
                      <li><span class="keyword">l2er:</span> Lab 2 end till. Use <code>l2er=end_time</code>.</li>
                    </ul>
                  </div>
                </div>
                <div class="example">
                    <div class="section-title">Example</div>
                    <div class="data">
                        <p>Here is an example of how you can use the keywords to search for courses:</p>
                        <p><code>c=cse110&i=taw</code></p>
                        <p>This search will return all courses in the CSE110 course which is taken by <a href="https://www.youtube.com/@LearnWithTawhid/videos">Tawhid Anwar</a> Sir.</p>
                        <p><code>c=cse220&c1er=10:00am&c1=sunday</code></p>
                        <p>This search will return all courses in the CSE220 course which take place in sunday and start from 10 am.</p>
                    </div>
              </div>
            </body>
            </html>
        """
        self.webview.setHtml(html_content)

        self.main_layout.addWidget(self.webview)
