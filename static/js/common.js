function submitClick(){
	if(document.getElementById('username').value.length==0){    
        alert('姓名输入不能为空！');
        document.getElementById('username').focus();
        return false;
    }
	else{
		if(document.getElementById('age').value.length==0){    
			alert('年龄输入不能为空！');
			document.getElementById('age').focus();
			return false;
		}
		else{
			if(document.getElementById('gender').value.length==0){    
				alert('性别输入不能为空！');
				document.getElementById('gender').focus();
				return false;
			}
			else{
				if(document.getElementById('starsign').value.length==0){    
					alert('星座输入不能为空！');
					document.getElementById('starsign').focus();
					return false;
				}
				else{
					if(document.getElementById('area').value.length==0){    
						alert('省市地区输入不能为空！');
						document.getElementById('area').focus();
						return false;
					}else
					{
					 document.getElementById("main").submit()
					}
				}
			}
		}
	}
}