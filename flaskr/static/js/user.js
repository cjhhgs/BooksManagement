axios.get("/bookmanage/record")
    .then(function(response){
        console.log(response)
        var user = new Vue({
            el: "#user",
            data:{
                records:response.data.record
            },
            methods:{
                returnBook:function(record){
                    var _this = this
                    var config = {
                        way:"returnBook",
                        info:{"record_id":record[0],"username":record[1],"book_id":record[2]}
                    }
                    axios.post("/bookmanage/database",config)
                        .then((response)=> {
                            console.log(response);
                            var returnStatu = response.data
                            if (returnStatu.statu == 0) {
                                alert(returnStatu.info)
                            }
                            else{
                                alert('error')
                            }
                        })
                        .catch((response) => {
                            console.log(response);
                        }).then(function(){
                            axios.get("/bookmanage/record")
                                .then((response) =>{
                                    _this.records = response.data.record
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })
                }
            }
        })
    })