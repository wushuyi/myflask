$.fn.markdown.messages.zh = {
    'Bold': "粗体",
    'Italic': "斜体",
    'Heading': "标题",
    'URL/Link': "链接",
    'Image': "图片",
    'List': "列表",
    'Unordered List': "无序列表",
    'Ordered List': "有序列表",
    'Code': "代码",
    'Quote': "引用",
    'Preview': "预览",
    'strong text': "粗体",
    'emphasized text': "强调",
    'heading text': "标题",
    'enter link description here': "输入链接说明",
    'Insert Hyperlink': "URL地址",
    'enter image description here': "输入图片说明",
    'Insert Image Hyperlink': "图片URL地址",
    'enter image title here': "在这里输入图片标题",
    'list text here': "这里是列表文本",
    'code text here': "这里输入代码",
    'quote here': "这里输入引用文本"


};

marked.setOptions({
    renderer: new marked.Renderer(),
    gfm: true,
    tables: true,
    breaks: true,
    pedantic: true,
    sanitize: true,
    smartLists: true,
    smartypants: true,
    highlight: function (code, type) {
        if (type) {
            return hljs.highlight(type, code).value;
        } else {
            return hljs.highlightAuto(code).value;
        }
    }
});

var markdownParser = function markdownParser(val) {
    var html = marked(val);
    var $html = $('<div>', {
        'html': html
    });
    $html.find('pre').each(function (_, pre) {
        var $pre = $(pre);
        var lang = $pre.children('code').attr('class').split('-')[1];
        $pre.addClass('hljs').addClass(lang);
    });
    return $html.html();
};

var $editor = $('#markdown');
$editor.markdown({
    //savable: true,
    language: 'zh',
    resize: 'both',
    parser: markdownParser,
    //onShow: function (self) {
    //    self.setContent($('#tmpl').html());
    //},
    onPreview: function (self) {
        setTimeout(function () {
            var $preview = self.$editor.find('div[data-provider="markdown-preview"]');
            $preview.addClass('markdown-body');
        }, 0);
    },
    //onSave: function(self){
    //    var data = {};
    //    var res = self.getContent();
    //    data.markdown = res;
    //    data.html = markdownParser(res);
    //    console.log(data);
    //}
});
var markdown_editor = $editor.data('markdown');
$('.submit-row input[type="submit"]').on('click', function (evt) {
    evt.preventDefault();
    var res = markdown_editor.getContent();
    var html = markdownParser(res);
    $('#content').val(html);
    $(this).closest('form').submit();
});