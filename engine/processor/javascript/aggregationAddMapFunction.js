function map(){
    var value = this.value;
    var tag = this._id;
    emit(tag,value)
}