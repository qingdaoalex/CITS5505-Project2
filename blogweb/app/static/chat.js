//在聊天框按下回车事件处理
function onKeyPress(e){
  var keyCode = null;
  if(e.which)
      keyCode = e.which;
  else if(e.keyCode)
      keyCode = e.keyCode;

  //如果按下回车
  if(keyCode == 13) {
      // 获取输入框中的问题
      var question_box = document.getElementById('question')
      var question = question_box.value
      //清空输入框内容并禁用输入框
      question_box.value = ""
      question_box.setAttribute("disabled","disabled")
      //不要问我为什么不隐藏这个:）
      var api_key = "78c33a07808c7b9e1905c89c88b3be14"
      var api_secret = "q707tevnk00f"

      // 通过XHR发送一个GET请求
      var xhr = new XMLHttpRequest()
      xhr.open('GET','http://i.itpk.cn/api.php?question='+encodeURIComponent(question)+"&api_key="+api_key+"&api_secret="+api_secret)
      xhr.onload = function(){
          //启用输入框
          question_box.removeAttribute('disabled');
          //获取对话框
          var live2d_dialog = document.getElementsByClassName("live2d-widget-dialog")[0]
          //显示对话框并把获取到的内容显示在对话框上
          live2d_dialog.style.opacity=1
          live2d_dialog.innerHTML = this.responseText
          //五秒后隐藏对话框
          window.setTimeout(()=>{
              live2d_dialog.style.opacity=0
          }, 5000);
      }
  }
}
