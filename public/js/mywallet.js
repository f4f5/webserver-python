/**
 * load table data from server and render to table.
 * @param {string} url request url from server.
 * @param {Object} data_des  describe how to load data if the data is too big
 * @param {function} renderFun  render function if data receive succeed
 * @param {selector} selector  css selector to descripe where to push the table's row data.
 * @return {void} 
 */
var loadDataAndRender = function(url, data_des, renderFun, selector){
    $.post(url, data_des,
    function(data,status){
        if(status=='success'){
            renderFun(data, selector);
        }
    });    
}

var tableCreator = function(n){
    var str = '<tr>\
        <th scope="row">{0}</th>\
        ';
    for(var i=1;i<n;i++){
        str+='<td>{'+i+'}</td>\
        ';
    }            
    str+='\
    </tr>\
    ';
    return str;
}

var renderTable = function(data, selector){
    var cell=[];   
    for(var index in data){
        cell=data[index];
        $(selector).append(tableCreator(cell.length).format(cell));
    }
}