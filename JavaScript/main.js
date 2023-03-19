const jUser='{"Token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NWU0YTkwZS03YmY4LTRiMWUtOGQzYy1mYzk1ZTczZDE2YWYiLCJuYW1lIjoi5rWL6K-VNSIsImp0aSI6IjcyZjlhODkxLTlhY2ItNGVmMC05ZGNkLTE2NzcxMDhlMGM1ZiIsImNvZGUiOiIxMzEwMDAwMDAwNCIsInR1dWlkIjoiMjU2NjQ5M2ItNDc5NS00ZmZkLTg4YjgtODlmNjU4MDJlZDdlIiwidG5hbWUiOiLmtYvor5Xnp5_miLciLCJ0Y29kZSI6IlZJUDIwMjIwODAwMDIiLCJpc3NhIjoiRmFsc2UiLCJpc2FkbWluIjoiRmFsc2UiLCJleHAiOjE2Nzk0Njc4ODUsImlzcyI6ImFjY291bnQuam9pbnYzIiwiYXVkIjoiam9pbnYzIn0.pDWykrVhPwKu85hBkHyYJj7fBHQKIBuJTI82qRN7PcY","UserData":[{"Key":"jt-bc","Value":"CN0001"}]}'
const jArg='{"Year": 2023,"Month": 3}';

// var x=require('./X');
// async function run(){
//     const r=await x(out,jUser,jArg);
//     function out(_,result){
//         console.log("result",result);
//     }
// }

// run();

var v = require('./V');
async function run() {
    const r = await v(out, jUser, jArg);
    function out(_, result) {
        console.log("result", result);
    }
}
run();
