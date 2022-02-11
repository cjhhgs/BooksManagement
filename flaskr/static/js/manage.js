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
                itemIndex:0,
                modifyTemp:{},
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

                setModifyTemp:function(item){
                    this.modifyTemp={};
                    for (var x = 0; x < item.length; x++) {
                        this.$set(this.modifyTemp, this.lables[x], item[x]);
                        
                    }
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
                addItem:function(){

                },

                deleteItem:function(item){
                    var _this = this;
                    config = {
                        way : "deleteItem",
                        info : {
                            table:_this.table,
                            id:item[0]
                        }
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
                            axios.get("/bookmanage/database?table="+_this.table)
                                .then((response) =>{
                                    _this.lables = response.data.lables
                                    _this.content = response.data.content
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })
                },

                modifyItem:function(item){
                    
                    this.setModifyTemp(item);
                    this.modifyFlag=true

                },

                submitModify:function(){

                },
                closeModifyPage:function(){

                }
            }
        })
    })