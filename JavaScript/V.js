//调试
const ENV={host:'v3.mealcloud.link',port:9443};
const requestSync=require('https');

//发布
// const ENV={host:'joinmcl-extjs-bff',port:80};
// const requestSync=require('http');

let tableData=function(obj,args){
    let BcProjectList = obj.BcProjectList;
    let RcInspectionRecordList = obj.RcInspectionRecordList;
    var days = new Date(args.Year, args.Month, 0).getDate();
    var columns = 6;
    var projectNamelist = ["菜品上传","能源关闭","晨检","周例会","每周大扫除","安全大检查"];
    let countJson = "";
    var bcArr = new Array();
    var safetyInspectionDay = "";

    // 获取项目点
    for(i = 0;i < BcProjectList.length;i++){
        bcArr[i] = [BcProjectList[i].BcCode,BcProjectList[i].BcName];
    }    

    //周日期处理
    var wDate = new Date(args.Year, args.Month - 1, 0)
    let dDay = wDate.getDay() > 0 ? wDate.getDay() : 7;
    let first = wDate.getDate() - dDay + 1;
    let week = new Date(wDate.setDate(first));
    var weekArr = new Array();
    // var weekArr = [[args.Month,1,args.Month.toString()+"/1"]]
    for (i = 0;i < 5;i++){
        week = new Date(wDate.setDate(week.getDate()+7));
        // if(week.getMonth()+1 == args.Month && week.getDate() != 1){
        if(week.getDate() != 1){
            weekArr.push([week.getFullYear(),week.getMonth()+1,week.getDate(),(week.getMonth()+1)+'/'+week.getDate()]);
        }
        if(week.getMonth() == args.Month){
            break;
        }
    }


    //考评项目循环
    for (pno = 0;pno < projectNamelist.length;pno++){

        var inspectionRecordArr = new Array();
        var NoHolidayNum = pno == 5 ? 1 : obj.NoHolidayNum;
        var Multiple = pno == 2 || pno == 4 ? 10 : 20;

        //处理巡检数据
        for (i = 0;i < RcInspectionRecordList.length;i++){
            if(RcInspectionRecordList[i].InspectionItemName == projectNamelist[pno]){
                if(pno == 0 || pno == 1 || pno == 5){
                    var rirmonth = new Date(RcInspectionRecordList[i].InspectionDate).getMonth()+1;
                    if(rirmonth == args.Month){
                        inspectionRecordArr.push([RcInspectionRecordList[i].Code,RcInspectionRecordList[i].InspectionItemName,RcInspectionRecordList[i].InspectionDate,RcInspectionRecordList[i].Scores,RcInspectionRecordList[i].BcCode]);
                    }
                }else{
                    inspectionRecordArr.push([RcInspectionRecordList[i].Code,RcInspectionRecordList[i].InspectionItemName,RcInspectionRecordList[i].InspectionDate,RcInspectionRecordList[i].Scores,RcInspectionRecordList[i].BcCode]);
                }
            }   
        }

        // 菜品上传&能源关闭&安全大检查
        if(pno == 0 || pno == 1 || pno == 5){
            for(i = 0;i < bcArr.length;i++){
                var scores = 0;
                for (j = 0;j < inspectionRecordArr.length;j++){
                    if(BcProjectList[i].BcCode == inspectionRecordArr[j][4]){
                        // scores += +inspectionRecordArr[j][3];
                        scores++;
                    }
                }
                bcArr[i][pno+2] = (scores*Multiple/NoHolidayNum).toFixed(2);
            }
        // 晨检&周例会&每周大扫除
        }else{
            for (i1 = 0;i1 < bcArr.length;i1++){
                var scores = 0;
                for (i2 = 0;i2 < columns;i2++){ 
                    var t_value = weekArr.length-1 > i2 ? "×" : "";
                    for (i3 = 0;i3 < inspectionRecordArr.length;i3++){
                        var riryear = new Date(inspectionRecordArr[i3][2]).getFullYear();
                        var rirmonth = new Date(inspectionRecordArr[i3][2]).getMonth()+1;
                        var rirday = new Date(inspectionRecordArr[i3][2]).getDate();
                        if (weekArr.length-1 > i2 && new Date(weekArr[i2+1][0],weekArr[i2+1][1],weekArr[i2+1][2]) > new Date(riryear,rirmonth,rirday) && new Date(riryear,rirmonth,rirday) >= new Date(weekArr[i2][0],weekArr[i2][1],weekArr[i2][2]) && bcArr[i1][0] == inspectionRecordArr[i3][4]) {
                            t_value = "√";
                        } 
                    }
                    scores = t_value == "√" ? scores + 1 : scores;
                }
                bcArr[i1][pno+2] = (scores*Multiple/4).toFixed(2);
    
            }
        }
        // 安全大检查日期获取
        if(pno == 5){
            for (i = 1;i < days;i++){
                var isDate = 0;
                for(j = 0;j<inspectionRecordArr.length;j++){
                    var rirday = new Date(inspectionRecordArr[j][2]).getDate();
                    if(rirday == i){
                        safetyInspectionDay = i+"日安全大检查";
                        break;
                    }
                }
                if(safetyInspectionDay != ""){
                    break;
                }
            }
        }
        

        
    }
    
    // 生成表内容
    for (i = 0;i < bcArr.length;i++){
        var tableArr = [["IsHeader",0],["t0",bcArr[i][1]],["t1",bcArr[i][2]],["t2",bcArr[i][3]],["t3",bcArr[i][4]],["t4",bcArr[i][5]],["t5",bcArr[i][6]],["t6",bcArr[i][7]],["t7",(parseFloat(bcArr[i][2])+parseFloat(bcArr[i][3])+parseFloat(bcArr[i][4])+parseFloat(bcArr[i][5])+parseFloat(bcArr[i][6])+parseFloat(bcArr[i][7])).toFixed(2)]];
        const tableArrObj = Object.fromEntries(tableArr);
        countJson = countJson == "" ? JSON.stringify(tableArrObj) : countJson +','+ JSON.stringify(tableArrObj);
    }

        return{
            headerData:safetyInspectionDay,
            countData:'['+countJson+']'
          }

}

let syncPost=function(user,args){
    
    return new Promise(function(resolve,reject){
        var content=JSON.stringify({
            'Year':args.Year,
			"Month": args.Month
        });
        
        var bcCode="";
        let bc=user.UserData.find(d=>d.Key=="jt-bc");
        if(bc) bcCode=bc.Value;

        var options={
            host:ENV.host,
            port:ENV.port,
            path:'/b010/InspectionManageMent/SearchRcInspectionReport',
            method:'POST',
            headers:{
                "Content-Type":'application/json; charset=utf-8',
                "Content-Length":content.length,
                "Authorization":'Bearer '+user.Token,
				"jt-bc":bcCode
            }
        };

        let req= requestSync.request(options,function(res){
            var _data='';
            res.on('data',function(chunk){
                _data+=chunk;
            });
            res.on('end',function(){
                resolve(_data);
            });
        });
        req.on('error',function(e){
            console.error(e);
            reject(e);
        });
        req.write(content);
        req.end();
    });
}

module.exports =async function (callback,jUser,jArgs){
    let user=JSON.parse(jUser);
    let args=JSON.parse(jArgs); 
    let x=async function(){
        let body=await syncPost(user,args);
        let obj=JSON.parse(body).Data;
        console.time('test')
        let data = tableData(obj,args);
        let headerData = data.headerData;
        let countData = JSON.parse(data.countData);
        var month = args.Month;
        var year = args.Year;
        return JSON.stringify({year,month,headerData,countData});
    }
    var result=await x();
    callback(null,result);
    console.timeEnd('test')
}