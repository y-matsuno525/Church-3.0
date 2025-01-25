function bindAnnotationForm() {
    $(".annotationForm").off("submit").on("submit", function (e) { //off("submit")がないと更新のたびにリクエストが増えていくかも
        e.preventDefault(); // フォームのデフォルト送信を無効化

        var formData = $(this).serialize(); // フォームデータをシリアライズ

        $.ajax({
            url: $(this).attr("action"), // フォームのaction属性を使用
            method: "POST",
            data: formData,
            success: function (response) {
                if (response.success) {
                    $("#annotationsContainer").html(response.html);
                    bindAnnotationForm();//【重要】再バインド。これがないと更新されたhtmlでbindAnnotationFormが使えない
                    alert("データが正常に保存されました: " + response.message);
                } else {
                    alert("エラー: " + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("エラーが発生しました:", error);
                alert("サーバーとの通信に失敗しました。");
            }
        });
    });
}

// 初回ロード時にイベントをバインド
$(document).ready(function () {
    bindAnnotationForm();
});