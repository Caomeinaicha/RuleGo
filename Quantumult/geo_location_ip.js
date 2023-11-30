  var url = "https://api.ip.sb/geoip"
  var opts = {
      policy: $environment.params
  };
  var myRequest = {
      url: url,
      opts: opts,
  };
 
  var message = ""
  const paras = ["ip","isp","country_code","city"]
  const paran = ["IP","ISP","地区","城市"]
  $task.fetch(myRequest).then(response => {
    message = response? json2info(response.body,paras) : ""
      $done({"title": "", "htmlMessage": message});
  }, reason => {
    message = "</br></br>查询超时"
    message = `<p style="text-align: center; font-family: -apple-system; font-size: large; font-weight: bold;">` + message + `</p>`
      $done({"title": "", "htmlMessage": message});
  })


function json2info(cnt,paras) {
  var res = ""
  cnt =JSON.parse(cnt)
  for (i=0;i<paras.length;i++) {
    cnt[paras[i]] = paras[i] == "country_code"? cnt[paras[i]]:cnt[paras[i]]
    res = cnt[paras[i]]?   res +"</br><b>"+ "<font  color=>" +paran[i] + "</font> : " + "</b>"+ "<font  color=>"+cnt[paras[i]] +"</font></br>" : res
  }
  res =res+ ""+"</br>" + $environment.params+ "</font>"
  res =  `<p style="text-align: center; font-family: -apple-system; font-size: large; font-weight: thin">` + res + `</p>`
  return res
}