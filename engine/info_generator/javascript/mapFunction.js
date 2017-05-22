function map(){
    var urls = this.urls;

    for(var i=0; i<urls.length; i++) {

        var expanded_url = urls[i].expanded_url;
        if(expanded_url.length > 1023)
            expanded_url = urls[i].url;

        emit(expanded_url, 1);
    }

}