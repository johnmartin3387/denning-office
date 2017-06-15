var FormBuilder_tp = function() {

    // initialize the global values
    let mode = 0
    let edit_form_mode = 0
    var formBuilder = null
    var jsonData = null

    var jsonDataForDB = []
    var form_type = ""

    var handleDemo = function() {
        $(".edit-tool").attr("style", "display:none;")
    }

    var saveFrame = function(type){
        if(mode == 0){
            mode = 1
            $(".edit-btn").html("Save Form")
            $(".edit-tool").attr("style", "")
        }
        else{
            mode = 0
            $(".edit-btn").html("Edit Form")
            $(".edit-tool").attr("style", "display:none;")

            if(form_type != ""){
                commitData(jsonDataForDB)
            }
        }
        form_type = type
    }
    
    var appendForm = function(obj, clss){
        str = '<div class="portlet box purple custom-form-item"> \
                <div class="portlet-title"> \
                    <div class="caption"> \
                         <span class="header-static" style=""></span> <input type="text" class="form-control input-sm header-edit" style="display: none"> </div> \
                    <div class="tools"> \
                        <a href="" class="collapse"> </a> \
                        <a href="" class="fullscreen edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.editForm(this)"> </a> \
                        <a href="javascript:;" class="edit-form edit-tool" onclick="FormBuilder_tp.appendForm(this, \'col-md-6\')"> </a> \
                        <a href="javascript:;" class="remove-form edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.removeForm(this)"> </a> \
                    </div> \
                </div> \
                <div class="portlet-body form"> \
                        <div class="form-body"> \
                        </div> \
                </div> \
            </div>'
        $(str).insertAfter($(obj).parent().parent().parent())
    }

    var getIDByObj = function(obj){
        return $(obj).parent().parent().next().children().eq(0).attr("for")
    }

    var editForm = function(obj, type){
        var header_static = $(obj).parent().prev().children().eq(0)
        var header_edit = $(obj).parent().prev().children().eq(1)

        if(edit_form_mode == 0){
            var id = getIDByObj(obj)
            if(id == undefined){
                randNum = genRand().toString()
                str = '<div class="row" id="myformbuilder-'+ randNum +'"> \
                    </div>'
            } else {
                str = '<div class="row" id="'+ id +'"> \
                    </div>'
            }
            $(obj).parent().parent().next().children().eq(0).html(str)
            $(obj).parent().parent().next().children().eq(0).attr("for", id)

            formBuilder = getFormBuilder(id);
            edit_form_mode = 1

            header_static.attr("style", "display:none;")
            header_edit.attr("style", "display:block;")
            header_edit.val(header_static.html())
        }else{
            $(obj).parent().parent().next().children().eq(0).html("")
            edit_form_mode = 0

            if(formBuilder != null){
                jsonData = formBuilder.actions.getData('json', true)

                json = convertBJsonToRJson(jsonData)
                html = convertJsonToHtml(json)

                updateData(getIDByObj(obj), header_edit.val(), JSON.parse(jsonData))

                $(obj).parent().parent().next().children().eq(0).html(html)

                $(".form_datetime").datetimepicker({
                    autoclose: true,
                    isRTL: App.isRTL(),
                    format: "dd MM yyyy - hh:ii",
                    pickerPosition: (App.isRTL() ? "bottom-right" : "bottom-left")
                });

                $('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
                // Workaround to fix datetimepicker position on window scroll
                $( document ).scroll(function(){
                    $('.form_datetime').datetimepicker('place'); //#modal is the id of the modal
                });

                $('.defaultrange_modal').daterangepicker({
                        opens: (App.isRTL() ? 'left' : 'right'),
                        format: 'MM/DD/YYYY',
                        separator: ' to ',
                        startDate: moment().subtract('days', 29),
                        endDate: moment(),
                        minDate: '01/01/2012',
                        maxDate: '12/31/2018',
                    },
                    function (start, end) {
                        $('.defaultrange_modal input').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                    }
                ); 

                header_static.attr("style", "display:block;")
                header_edit.attr("style", "display:none;")
                header_static.html(header_edit.val())
            }
        }
    }

    var removeForm = function(obj){
        if(getIDByObj(obj) != undefined){
            removeData(getIDByObj(obj))
        }

        $(obj).parent().parent().parent().remove()
    }

    var getCustomForm = function(json){
        var res = ""
        jsonDataForDB = json
        for(var i=0; i<json.length; i++){
            var str = '<div class="portlet box purple custom-form-item"> \
                        <div class="portlet-title"> \
                            <div class="caption"> \
                                 <span class="header-static" style="">'+ json[i][2] +'</span> <input type="text" class="form-control input-sm header-edit" style="display: none"> </div> \
                            <div class="tools"> \
                                <a href="" class="collapse"> </a> \
                                <a href="" class="fullscreen edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.editForm(this)"> </a> \
                                <a href="javascript:;" class="edit-form edit-tool" onclick="FormBuilder_tp.appendForm(this, \'col-md-6\')"> </a> \
                                <a href="javascript:;" class="remove-form edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.removeForm(this)"> </a> \
                            </div> \
                        </div> \
                        <div class="portlet-body form form-horizontal"> \
                                <div class="form-body" for="'+json[i][0]+'"> ' +
                                convertJsonToHtml(json[i][1])
                                + ' \
                                </div> \
                        </div> \
                    </div>'
            res += str
        }
        return res
    }

    var setMode = function(param){
        mode = param
        if(mode == 0){
            mode = 1
            $(".edit-btn").html("Save Form")
            $(".edit-tool").attr("style", "")
        }
        else{
            mode = 0
            $(".edit-btn").html("Edit Form")
            $(".edit-tool").attr("style", "display:none;")
        }
    }

    var getFormBuilder = function(indicator){
        var options = {
          disabledAttrs: ["value", "className", "name", "access", "help", 
                    "inline", "other", "style", "toggle"],
          disabledActionButtons: ['data', 'clear', 'save'],
          typeUserAttrs: {
            autocomplete: {
              className: {
                label: 'Type',
                options: {
                  'red form-control': 'Red',
                  'green form-control': 'Green',
                  'blue form-control': 'Blue'
                }
              }
            },
            date: {
              className: {
                label: 'Type',
                options: {
                  'single': 'Single',
                  'range': 'Range'
                }
              }
            },
            
          }
        };

        var data = getData(indicator);
        console.log(indicator)
        console.log(data)
        if(data != undefined){
            options["defaultFields"] = data
        }

        return $("#" + indicator).formBuilder(options);
    }

    var genRand = function() {
      return Math.floor(Math.random()*89999+10000);
    }

    var slugify = function(string) {
      return string
        .toString()
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-]+/g, "")
        .replace(/\-\-+/g, "-")
        .replace(/^-+/, "")
        .replace(/-+$/, "");
    }

    // convert FormBuilder Json into the json data for metronics form
    var convertBJsonToRJson = function(jsonData){
        jsonData = JSON.parse(jsonData)
        for(var idx=0; idx<jsonData.length; idx++){
            console.log(jsonData[idx])
        }
        return jsonData
    }

    var getInputStr = function(element, placeholder){
        var type = element["subtype"]
        if(type == undefined)
            type = element["type"]

        var html = '<div class="form-group form-md-line-input has-success"> \
            <label class="col-md-4 control-label">'+ element["label"] +'</label> \
            <div class="col-md-8"> \
                <input type="' + type + '" class="form-control" placeholder="'+ placeholder +'" name="'+ slugify(element['label']) +'"> \
                <div class="form-control-focus"> </div> \
            </div> \
        </div>'

        return html
    }

    var getButtonStr = function(element, placeholder){
        var html = '<a href="javascript:;" class="btn default"> Link </a>'
    }

    var getDateStr = function(element, placeholder){
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8">\
                        <div class="input-group input-large form_datetime"> \
                            <input type="text" placeholder="'+ placeholder +'" name="'+ slugify(element['label']) +'" class="form-control date-set"> \
                        </div> \
                        </div> \
                    </div>'

        return html
    }

    var getDateRangeStr = function(element, placeholder){
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <div class="input-group input-large defaultrange_modal"> \
                                <input type="text" class="form-control"> \
                                <span class="input-group-btn"> \
                                    <button class="btn default date-range-toggle" type="button"> \
                                        <i class="fa fa-calendar"></i> \
                                    </button> \
                                </span> \
                            </div> \
                        </div> \
                    </div>'

        return html
    }

    var getTextareaStr = function(element, placeholder){
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <textarea class="form-control" rows="3" placeholder="'+ placeholder +'" name="'+ slugify(element['label']) +'"> </textarea> \
                        </div> \
                    </div>'

        return html
    }

    var getCheckboxStr = function(element, placeholder){
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <input type="checkbox" class="md-check" placeholder="'+ placeholder +'" name="'+ slugify(element['label']) +'"> \
                            <label for="interest"> \
                                <span></span> \
                                <span class="check"></span> \
                                <span class="box"></span></label> \
                        </div> \
                    </div>'

        return html
    }

    var getAutoCompleteStr = function(element, placeholder){
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8 input-group-control"> \
                            <div class="input-group input-group-sm">\
                            <div class="input-group-control"> \
                            <select class="form-control" name="'+ slugify(element['label']) +'"> \
                                <option value="">Option 1</option> \
                                <option value="">Option 2</option> \
                                <option value="">Option 3</option> \
                                <option value="">Option 4</option> \
                            </select> \
                            </div> \
                            <span class="input-group-btn btn-right"> \
                                <a href="javascript:;" class="btn btn-icon-only blue"> \
                                    <i class="fa fa-search"></i> \
                                </a> \
                            </span> \
                            </div> \
                        </div> \
                    </div>'
        return html
    }

    var getSelectStr = function(element, placeholder){
        var options = ""
        if(element["values"] != undefined){
            for(var index=0; index<element["values"].length; index++){
                options += '<option value="'+ element["values"][index]["value"] 
                    +'">'+ element["values"][index]["label"] +'</option>'
            }
        }

        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <select class="form-control" name="'+ slugify(element['label']) +'"> \
                                '+ options +' \
                            </select> \
                        </div> \
                    </div>'
                    
        return html
    }

    // convert json data into html string
    var convertJsonToHtml = function(jsonData){
        var html = ""
        for(var idx=0; idx<jsonData.length; idx++){
            element = jsonData[idx]
            var placeholder = element["placeholder"]
            if(placeholder == undefined)
                placeholder = ""

            // for input element
            if(element["type"] == "text" || element["type"] == "number"){
                html += getInputStr(element, placeholder)
            } else if(element["type"] == "date" && element["className"] == "single"){
                html += getDateStr(element, placeholder)
            } else if(element["type"] == "date" && element["className"] == "range"){
                html += getDateRangeStr(element, placeholder)
            } else if(element["type"] == "textarea"){
                html += getTextareaStr(element, placeholder)
            } else if(element["type"] == "checkbox-group"){
                html += getCheckboxStr(element, placeholder)
            } else if(element["type"] == "autocomplete"){
                html += getAutoCompleteStr(element, placeholder)
            } else if(element["type"] == "select"){
                html += getSelectStr(element, placeholder)
            }
                
        }
        return html
    }

    var updateData = function(key, header, data){
        var flag = 0, i = 0;

        if(data.length == 0)
            return

        for(i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                flag = 1
                break
            }
        }

        if(flag == 1){
            jsonDataForDB.splice(i, 1, [key, data, header]);
        } else {
            jsonDataForDB.push([key, data, header]);
        }
    }

    var commitData = function(json){
        alert(JSON.stringify(json))
        // commit json data into server
        if(form_type == "contact"){
            if($("#type").val() == "new"){
                var name = $("#new_type").val()
                $.ajax({
                    type: 'post',
                    url: '/api/contact_template/',
                    data: JSON.stringify({"type": name, "json": JSON.stringify(json)}),
                    contentType: 'application/json; charset=UTF-8',
                    dataType: 'json',
                    success: function(data) {
                      
                    }
                });
            } else {
                $.ajax({
                    type: 'put',
                    url: '/api/contact_template/'+$("#type").val()+'/?format=json',
                    contentType: 'application/json; charset=UTF-8',
                    data: JSON.stringify({"json": JSON.stringify(json)}),
                    dataType: 'json',
                    success: function(data) {
                      
                    }
                });
            }
        }
    }

    var removeData = function(key){
        for(var i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                jsonDataForDB.splice(i, 1);
                break
            }
        }
    }

    var getData = function(key){
        for(var i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                return jsonDataForDB[i][1]
            }
        }
    }

    return {
        //main function to initiate the module
        init: function() {
            handleDemo();
        },
        appendForm: function(obj, clss) {
            appendForm(obj, clss);
        },
        editForm: function(obj, type) {
            editForm(obj, type);
        },
        removeForm: function(obj) {
            removeForm(obj);
        },
        saveFrame: function(type) {
            saveFrame(type);
        },
        commitData: function(json) {
            commitData(json);
        },
        getCustomForm: function(json){
            return getCustomForm(json)
        },
        setMode: function(param){
            setMode(param)
        }
    };

}();

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function() {
        FormBuilder_tp.init();
    });
}
