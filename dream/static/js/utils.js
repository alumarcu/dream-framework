"use strict";

var dream = dream || {};

dream.utils = {
    /**
     * Retrieves the value of a cookie
     * @param name
     * @returns {*}
     */
    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    /**
     * @param method
     * @returns {boolean}
     */
    csrfSafeMethod: function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },
    /**
     * Callback for ajax beforeSend that sets the header with CSRF token
     */
    setCsrfToken: function() {
        return function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', dream.utils.getCookie('csrftoken'));
        }
    }
};
