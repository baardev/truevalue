"use strict";
function wpucv_change_page(list_id, wrapper_id, page){
	
	if('none' != list_id){
		jQuery.ajax({
			url: wpucv_admin_url,
			method: 'POST',
			dataType: 'json',
			data: {
				action: 'wpucv_get_list_page',
				list_id: list_id,
				wrapper_id: wrapper_id,
				page: page
			},
			success: function(data){
				"use strict";
				if(data && data.list){
					jQuery('#' + wrapper_id + ' .wpucv-list-wrapper').fadeOut(500, function(){
						"use strict";
						jQuery('#' + wrapper_id + ' .wpucv-list-wrapper').html(data.list);
						jQuery('#' + wrapper_id + ' .wpucv-list-wrapper').fadeIn(500);
					});
				}
				if(data && data.pagination){
					jQuery('#' + wrapper_id + ' .wpucv-pagination-wrapper').html(data.pagination);
				}
			},
			error: function(){
				
			}
		});
	}
}
//-------------------------------------

