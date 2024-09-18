const jsdom = require("jsdom");
const { JSDOM } = jsdom;

// 创建一个新的 JSDOM 实例
const dom = new JSDOM(`<html><body></body></html>`, {
   url: "http://ipaper.pagx.cn/bz/html/index.html"
});
// 将全局对象设置为 jsdom 创建的对象
global.window = dom.window;
global.document = dom.window.document;
global.localStorage = dom.window.localStorage;
global.sessionStorage = dom.window.sessionStorage;

// 获取 window 对象
// const { window } = dom;
var _local = {
	//存储,可设置过期时间
	set(key, value, expires) {
		let params = { key, value, expires };
		if (expires) {
			// 记录何时将值存入缓存，毫秒级
			var data = Object.assign(params, { startTime: new Date().getTime() });
			localStorage.setItem(key, JSON.stringify(data));
		} else {
			if (Object.prototype.toString.call(value) == '[object Object]') {
				value = JSON.stringify(value);
			}
			if (Object.prototype.toString.call(value) == '[object Array]') {
				value = JSON.stringify(value);
			}
			localStorage.setItem(key, value);
		}
	},
	//取出
	get(key) {
		let item = "\"9195459e-c0be-47fd-8c0f-552e11cba122\"";
		// 先将拿到的试着进行json转为对象的形式
		try {
			item = JSON.parse(item);
		} catch (error) {
			// eslint-disable-next-line no-self-assign
			item = item;
		}
		// 如果有startTime的值，说明设置了失效时间
		if (item && item.startTime) {
			let date = new Date().getTime();
			// 如果大于就是过期了，如果小于或等于就还没过期
			if (date - item.startTime > item.expires) {
				localStorage.removeItem(name);
				return false;
			} else {
				return item.value;
			}
		} else {
			return item;
		}
	},
	// 删除
	remove(key) {
		localStorage.removeItem(key);
	},
	// 清除全部
	clear() {
		localStorage.clear();
	}
}

getUrlParam = function (name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}
function generateUUID() {
	var d = new Date().getTime();
	var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
		var r = (d + Math.random()*16)%16 | 0;
		d = Math.floor(d/16);
		return (c=='x' ? r : (r&0x3|0x8)).toString(16);
	});
	return uuid;
};

function getIdentity(){
	//带过来的唯一标识
	var myIdentity = getUrlParam("identity");
	if(null == myIdentity || undefined == myIdentity || "" == myIdentity){
		myIdentity = _local.get("1" + "identity");
	}else{
		_local.set("1" + "identity",myIdentity);
	}
	if(myIdentity == null || "" == myIdentity){
		myIdentity = generateUUID();
		_local.set("1" + "identity",myIdentity);
	}
	return myIdentity;
}

console.log(getIdentity());