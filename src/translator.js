var request = require('./api-request');
var c = require('./config');

function translate(text,from='auto',to='auto') {
  return doTranslate(
    text, from, to, $option.secret
  )
}

async function doTranslate(text,from, to,secret) {
  let config = c.getConfig();
  const url = config.api_url + '?keyword=' + text;

  try {
    let resp = await request.query({},url, 'GET');
    let data = parseResponse(resp.data,text);
    return Promise.resolve(data);
  } catch(err) {
    return Promise.reject(err);
  }
}

function parseResponse(data,text) {
  let additions = [];
	let phonetics = [];
	let exchanges = [];
	let parts = [];
	let toParagraphs = [];
	let fromParagraphs = [ text ];
  let relatedWordParts = [];
  let labels = [];

  let prons = data.pron|| [];
  for (let pron of prons) {
    phonetics.push({
        "type": pron.region,
        "value": pron.ipa,
        "tts": {
            "type": "url",
            "value": "https://dict.youdao.com/dictvoice?audio=" + text
        }
    })
  }

  let senses = data.senses || [];
  let sec = 1;
  for (let sense of senses) {
    let name = (sense.pos || 'u') + ".";
    if ("guideword" in sense) {
      name += " (" + sense.guideword + ")"; 
    }

    let definitions = sense.definitions || [];
    additions.push({ name: name,value: '-----' });
    
    for (let d of definitions) {
      let cn_def = `${sec}. ${d.cn_def || ''}`;
      let en_def = (d.en_def || '');

      let examples = d.examples || [];
      let exampleText = '';
      for (let i=0;i<examples.length;i++) {
        let ex = examples[i];
        exampleText += `[${sec}.${i+1}]: ${ex.en} (${ex.cn})\n`;
      }

      additions.push({ name: cn_def, value: en_def});
      additions.push({ name: "examples:", value: exampleText});

      sec += 1;
    }
  }

  return {
    toDict: {
      word: text,
      phonetics,
      parts,
      exchanges,
      additions,
      relatedWordParts
    },
    fromParagraphs,
    toParagraphs
  }
}


exports.translate = translate;