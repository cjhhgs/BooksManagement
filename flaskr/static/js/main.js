axios.get("/bookmanage/database?table=book_list")
    .then(function (response) {
        console.log(response)
        var booklist = new Vue({
            el: "#book",
            data: {
                lables:response.data.lables,
                content:response.data.content,
            },
            methods:{
                borrow: function(bookid){
                    var _this = this
                    
                    var config = {
                        way:"borrow",
                        info:bookid
                    }
                    axios.post("/bookmanage/database",config)
                        .then((response) => {
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
                            axios.get("/bookmanage/database?table=book_list")
                                .then((response) =>{
                                    _this.content = response.data.content
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })
                    
                }
            }
            
        })
    })
