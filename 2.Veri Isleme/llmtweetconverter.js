

const comments = [
  {
    "text": "%50 indirim bu şekilde oluyormuş."
  },
  {
    "text": "Mükerrer yaptığım ödemeden dolayı mağdur edildim."
  },
  {
    "text": "Sırf daha fazla para kazanmak için tüketicinin mağdur edilmesi hiç doğru değil."
  },
  {
    "text": "4.5 aylık bir telefonun 2 defa servise gitmesi normal midir, firmanın değişim yapması gerekmez mi?"
  },
  {
    "text": "Aradığınız kişiye ulaşılamıyor anonsunun ücret yazdığını belirttiler."
  },
  
];

// Promptu oluşturan fonksiyon
function createPrompt(commentGroup) {
    const formattedComments = commentGroup.map((c, index) => `${index + 1}. ${c.text}`).join("\n\n");
    return `Bu 5 mobil operatör şikayet metin özetine sikayetler hakkında en temek hashtagleri olustur ve sonuna ekle${formattedComments}

Data "tweet", "hashtags" formatında olsun:`;
}

// 5 yorumu birden işleyen fonksiyon
async function processCommentGroup(commentGroup, groupIndex) {
    const textarea = document.querySelector('#prompt-textarea');
    const sendButton = document.querySelector('[data-testid="send-button"]');
    
    // Promptu oluştur
    const prompt = createPrompt(commentGroup);
    
    // Textarea'yı temizle ve promptu yaz
    textarea.value = prompt;
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    
    // Gönder butonuna tıkla
    sendButton.click();
    
    console.log(`İşleme başladı: Yorum Grubu ${groupIndex + 1}`);
    
    // Cevabı bekle ve kontrol et
    let answer = null;
    const maxWaitTime = 100000; // 100sn
    const checkInterval = 1000; // Her saniye kontrol et
    const startTime = Date.now();
    
    while (!answer && Date.now() - startTime < maxWaitTime) {
        await new Promise(resolve => setTimeout(resolve, checkInterval));
        
        const answerDiv = document.querySelector('div.flex.items-center.relative.text-token-text-secondary.bg-token-main-surface-secondary');
        if (answerDiv && answerDiv.textContent.trim().startsWith('"')) {
            answer = answerDiv.nextElementSibling.textContent.trim();
            break;
        }
    }
    
    if (answer) {
        console.log(`İşlendi: Yorum Grubu ${groupIndex + 1}`);
        return answer;
    } else {
        console.error(`Cevap bulunamadı veya zaman aşımı: Yorum Grubu ${groupIndex + 1}`);
        return null;
    }
}

// Tüm yorumları 5'erli gruplar halinde işleyen ana fonksiyon
async function processAllComments() {
    const allResults = [];
    
    for (let i = 0; i < comments.length; i += 5) {
        const commentGroup = comments.slice(i, i + 5);
        console.log(`${i+1}-${Math.min(i+5, comments.length)} arası yorumlar işleniyor...`);
        const result = await processCommentGroup(commentGroup, i / 5);
        if (result) {
            allResults.push(result);
        }
        
        if (i + 5 < comments.length) {
            console.log("5 yorum işlendi, 1 dakika bekleniyor...");
            await new Promise(resolve => setTimeout(resolve, 60000)); // 1 dakika bekle
        }
    }
    
    console.log("Tüm işlemler tamamlandı. Sonuçlar:");
    allResults.forEach((result, index) => {
        console.log(`Yorum Grubu ${index + 1}:`);
        console.log(result);
        console.log('------------------------');
    });
}

// İşlemi başlat
processAllComments();