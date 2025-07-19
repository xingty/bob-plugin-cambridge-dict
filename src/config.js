const supportedLanguages = [
  ["auto", "auto"],
  ["en", "EN"],
  ["zh-Hans", "ZH"],
  ["zh-Hant", "ZH"],
];


exports.supportedLanguages = supportedLanguages;

exports.getConfig = function() {
  return {
    "api_url": $option.url,
    "secret": $option.secret
  }
}
