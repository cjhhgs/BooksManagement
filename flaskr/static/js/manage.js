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
                modifyIndex:0,
                oldInfo:[],
                newInfo:[],
                modifyTemp:{},
                displayFlag:false,
                modifyFlag:false,
                addFlag:false
                
            },
            methods:{
                chooseTable:function(index){
                    this.closeModifyPage();
                    var _this = this;
                    this.tableIndex = index;
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

                
                addItem:function(){
                    this.displayFlag=true;
                    this.addFlag=true;
                    this.modifyTemp={};
                    var item = Array(this.lables.length).fill("")
                    this.setModifyTemp(item)
                    this.displayFlag=true;
                    this.addFlag=true;
                    this.modifyFlag=false;
                },

                submitAdd:function(){
                    this.newInfo = [];
                    for (key in this.modifyTemp) {
                        this.newInfo.push(this.modifyTemp[key]);
                    }
                    config = {
                        way:"addItem",
                        info:{
                            table:this.tables[this.tableIndex],
                            item:this.newInfo
                        }
                    }
                    var _this = this;
                    axios.post("/bookmanage/database", config)
                        .then((response) => {
                            console.log(response);
                            var returnStatu = response.data
                            if (returnStatu.statu == 0) {
                                alert(returnStatu.info)
                                
                            }
                        })
                        .catch((response) => {
                            console.log(response);
                        }).then(function(){
                            _this.modifyFlag = false;
                            _this.displayFlag = false;
                            axios.get("/bookmanage/database?table="+_this.tables[_this.tableIndex])
                                .then((response) =>{
                                    _this.lables = response.data.lables
                                    _this.content = response.data.content
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })

                },

                deleteItem:function(item){
                    var _this = this;
                    config = {
                        way : "deleteItem",
                        info : {
                            table:_this.tables[_this.tableIndex],
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
                            axios.get("/bookmanage/database?table="+_this.tables[_this.tableIndex])
                                .then((response) =>{
                                    _this.lables = response.data.lables
                                    _this.content = response.data.content
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })
                },

                modifyItem:function(item,index){
                    this.oldInfo = item;
                    this.modifyIndex = index;
                    this.setModifyTemp(item);
                    this.displayFlag=true;
                    this.modifyFlag=true;
                    this.addFlag = false;
                },

                submitModify:function(){
                    var _this = this
                    this.newInfo = [];
                    for (key in this.modifyTemp) {
                        this.newInfo.push(this.modifyTemp[key]);
                    }
                    var config = {
                        way:"modifyItem",
                        info:{
                            table: this.tables[this.tableIndex],
                            oldInfo: this.oldInfo,
                            newInfo: this.newInfo
                        }
                    }
                    var res = false;
                    axios.post("/bookmanage/database", config)
                        .then((response) => {
                            console.log(response);
                            var returnStatu = response.data
                            if (returnStatu.statu == 0) {
                                alert(returnStatu.info)
                            }
                            res = true;
                        })
                        .catch((response) => {
                            console.log(response);
                        }).then(function(){
                            _this.modifyFlag = false;
                            _this.displayFlag = false;
                            axios.get("/bookmanage/database?table="+_this.tables[_this.tableIndex])
                                .then((response) =>{
                                    _this.lables = response.data.lables
                                    _this.content = response.data.content
                                })
                                .catch((response) => {
                                    console.log(response);
                                })
                        })
                },

                closeModifyPage:function(){
                    this.modifyFlag = false;
                    this.addFlag = false;
                    this.displayFlag = false;
                }

                
            }
        })
    })