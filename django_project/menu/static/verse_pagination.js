function bindPaginationEvents(container) {
    // ページ送りボタンのクリックイベント
    container.find(".pagination-button").off("click").on("click", function () {
        var chapterNumber = $(this).data("chapter-number");
        var ajaxUrl = container.data("ajax-url");
        var bookId = container.data("book-id");
        loadChapter(chapterNumber, ajaxUrl, bookId);
    });

    // セレクトボックスの変更イベント
    container.find(".chapter-selector").off("change").on("change", function () {
        var chapterNumber = $(this).val();
        var ajaxUrl = container.data("ajax-url");
        var bookId = container.data("book-id");
        loadChapter(chapterNumber, ajaxUrl, bookId);
    });
}

function loadChapter(chapterNumber, ajaxUrl, bookId) {
    // Ajaxリクエストを送信
    $.ajax({
        url: ajaxUrl,
        method: "GET",
        data: {
            book_id: bookId,
            chapter_number: chapterNumber
        },
        success: function (response) {
            if (response.html) {
                var container = $("#content-container");
                container.html(response.html); // 新しい章の内容を更新

                // 新しいコンテンツに対してイベントリスナーを再バインド
                bindPaginationEvents(container);

                window.scrollTo(0, 0);
            } else {
                alert("章の内容を取得できませんでした。");
            }
        },
        error: function () {
            alert("エラーが発生しました。");
        }
    });
}

// 初回ロード時にイベントをバインド
$(document).ready(function () {
    var container = $("#content-container");
    bindPaginationEvents(container);
});
