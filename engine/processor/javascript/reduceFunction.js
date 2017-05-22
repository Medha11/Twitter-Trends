function reduce(key, values){
    var total = 0;
    var set = {};
    var pseudos = [];
    for(var i=0; i<values.length; i++) {
        total += values[i].count;
        var temp = values[i].pseudos;

        for(var j=0; j<temp.length; j++)  {
           if(!(temp[j] in set)) {
               set[temp[j]] = true;
               pseudos.push(temp[j])
           }
        }

    }
    return {'pseudos': pseudos, 'count': total};
}