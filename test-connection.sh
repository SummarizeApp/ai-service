#!/bin/bash

URL="http://localhost:5000/summarize"

read -r -d '' DATA << EOM
{
  "text": "BAŞKAN : başkan1\nÜYE : üye1\nÜYE : üye2\nCUMHURİYET SAVCISI : savcı1\nKATİP : katip1\nBelirli gün ve saatte 4. celse açıldı. Katılan vekili Av. 1 geldi. \nAçık yargılamaya devam olundu. \nHeyet değişikliği nedeni ile önceki zabıtlar okundu.\nTanık kişi2 adına çıkartılan davetiyenin tebligat kanunun 21. Maddesine göre yapıldığı görüldü. \nSanık sanık1 adına çıkartılan yakalama emrinin infaz edilemediği görüldü. \nTanık kişi3 adına çıkartılan davetiyenin tebligat kanunun 21. Maddesine göre yapıldığı görüldü. \nKatılan vekilinden soruldu : Eksik hususlar giderilsin , zararımız giderilmemiştir dedi. \nİddia makamından soruldu: Eksik hususların giderilmesi talep olunur dedi. \nDosya incelendi;\nGEREĞİ GÖRÜŞÜLÜP DÜŞÜNÜLDÜ:\n1-Sanık sanık1 adına çıkartılan yakalama emrinin infazının beklenmesine, \n2-Tanık kişi2 ve kişi3'ün davetiye tebliğine rağmen gelmediğinden zorla getirilmelerine, \nBu nedenle duruşmanın 11/04/2017 günü saat 09:50 bırakılmasına karar verildi."
}
EOM

CONCURRENT_REQUESTS=2

make_request() {
    START=$(date +%s.%N)
    curl -X POST $URL \
        -H "Content-Type: application/json" \
        -d "$DATA" -o /dev/null -s
    END=$(date +%s.%N)
    DURATION=$(echo "$END - $START" | bc)
    echo "Yanıt süresi: $DURATION saniye"
}

for ((i = 1; i <= CONCURRENT_REQUESTS; i++)); do
    make_request &
done

wait

echo "Tüm istekler tamamlandı."
