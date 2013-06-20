// $(function(){
// 	$('ajax-search-field').change(function(){
// 		var $data = $(this).val();
// 		$.post('/ajax_reqs/autocomplete/',
// 				{send_data:data},
// 				function(response){

// 				}
// 			);
// 	});
// })

(function($) {
    $(function () {
        $("#ajax-search-field").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/ajax_reqs/autocomplete/",
                    data: {
                        filter: request.term,
                        pagesize: 10
                    },
                    jsonp: "jsonp",
                    dataType: "jsonp",
                    success: function(data) {
                        response($.map(data.users, function(el, index) {
                            return {
                                value: el.display_name,
                                avatar: '/media/' + el.display_pic,
                                id : el.id
                            };
                        }));
                    }
                });
            },
            
            select: function(e, ui){
                $('#ajax-search-field').attr("value",ui.item.id);
            }

        }).data("autocomplete")._renderItem = function (ul, item) {
            return $("<li />")
                .data("item.autocomplete", item)
                .append("<a><img class='image-autocomplete' src='" + item.avatar + "' />" + item.value + "</a>")
                .appendTo(ul);
        };    
    });
})(grp.jQuery);

