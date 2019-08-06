var loadDataAndRender = function(url, data_des, renderFun){
    $.post(url, data_des,
    function(data,status){
        if(status=='success'){
            renderFun(data);
        }
    });    
}
var renderTrade = function(data){
    var cell=[];
    for(var index in data){
        cell=data[index];
        $('#tradeTable').append(`
        <tr>
            <th scope="row">{0}</th>
            <td>{1}</td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
        </tr>
        `.format.apply(this, cell));
    }
}