function map(){
    var tags = this.entities;

    for(var i=0; i<tags.length; i++) {
        var lower = tags[i].toLowerCase()
        emit(lower, {'pseudos': [tags[i]], 'count': 1});
    }

}