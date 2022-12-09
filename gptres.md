$.ajax({
  type: "GET",
  url: "https://www.example.com/api/endpoint",
  success: function(response) {
    // API'dan dönen cevapla birlikte gelen "Content-Disposition" başlığını kontrol edin
    var disposition = response.getResponseHeader("Content-Disposition");
    if (disposition && disposition.indexOf("attachment") !== -1) {
      // "Content-Disposition" başlığı indirilebilir dosya içeriyorsa, dosya ismini ve uzantısını URL'ye dönüştürün ve bir "a" öğesi oluşturun
      var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
      var matches = filenameRegex.exec(disposition);
      if (matches != null && matches[1]) {
        var filename = matches[1].replace(/['"]/g, "");
        var url = URL.createObjectURL(response);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
      }
    } else {
      // "Content-Disposition" başlığı indirilebilir dosya içermiyorsa, dosya içeriğini bir değişkene atayın ve bir pop-up penceresinde gösterin
      var data = response;
      var newWindow = window.open();
      newWindow.document.write(data);
    }
  }
});



data = {
  "area_name": "example_area",
  "num_of_loc": 10,
  "is_normal_dist": True,
  "wb_or_xmean": 10.5,
  "eb_or_xstd": 2.5,
  "nb_or_ymean": 15.0,
  "sb_or_ystd": 3.0
}

$.ajax({
  type: "GET",
  url: "https://www.example.com/api/endpoint",
  data: data,
  success: function(response) {
    // API'dan dönen veriyi işleyin
  }
});