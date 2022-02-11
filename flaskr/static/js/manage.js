axios.get("/bookmanage/database?table=book_list")
    .then(function (response) {
        console.log(response)
        var manage = new Vue({
            el: "#manage",
            data:{
                lables:response.data.lables,
                content:response.data.content,
                tables:['book_list','user'],
                tableIndex:0,
                modifyFlag:false,
                
            },
            methods:{
                chooseTable:function(index){
                    var _this = this;
                    var table = this.tables[index];
                    axios.get("/bookmanage/database?table="+table)
                        .then((response) =>{
                            console.log(response);
                            _this.lables = response.data.lables;
                            _this.content = response.data.content;
                        })
                    const len = _this.lables.length;
                    tempItem = new Array(len).fill(0)
                    return 1
                },

                inputBook:function(){
                    var _this = this;
                    axios.get("/bookmanage/database?table=book_list")
                        .then((response) =>{
                            console.log(response);
                            _this.lables = response.data.lables
                        }).then(function(){
                            _this.table = 'book_list';
                            _this.modifyFlag = true;
                        })
                },
            }
        })
    })