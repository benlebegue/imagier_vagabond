import ClassicEditorBase from "@ckeditor/ckeditor5-editor-classic/src/classiceditor";
import EssentialsPlugin from "@ckeditor/ckeditor5-essentials/src/essentials";
import AutoformatPlugin from "@ckeditor/ckeditor5-autoformat/src/autoformat";
import BoldPlugin from "@ckeditor/ckeditor5-basic-styles/src/bold";
import ItalicPlugin from "@ckeditor/ckeditor5-basic-styles/src/italic";
import ParagraphPlugin from "@ckeditor/ckeditor5-paragraph/src/paragraph";
import HeadingPlugin from "@ckeditor/ckeditor5-heading/src/heading";
import BlockQuotePlugin from "@ckeditor/ckeditor5-block-quote/src/blockquote";
import ListPlugin from "@ckeditor/ckeditor5-list/src/list";
import AlignmentPlugin from "@ckeditor/ckeditor5-alignment/src/alignment";
import ImagePlugin from "@ckeditor/ckeditor5-image/src/image";
import AutoImagePlugin from "@ckeditor/ckeditor5-image/src/autoimage";
import ImageInsertPlugin from "@ckeditor/ckeditor5-image/src/imageinsert";
import ImageCaptionPlugin from "@ckeditor/ckeditor5-image/src/imagecaption";
import ImageResizePlugin from "@ckeditor/ckeditor5-image/src/imageresize";
import ImageToolbarPlugin from "@ckeditor/ckeditor5-image/src/imagetoolbar";
//import ImageStylePlugin from "@ckeditor/ckeditor5-image/src/imagestyle";
//import ImageUploadPlugin from "@ckeditor/ckeditor5-image/src/imageupload";
import LinkPlugin from "@ckeditor/ckeditor5-link/src/link";
import LinkImagePlugin from "@ckeditor/ckeditor5-link/src/linkimage";
import RemoveFormatPlugin from "@ckeditor/ckeditor5-remove-format/src/removeformat";
import SourceEditingPlugin from "@ckeditor/ckeditor5-source-editing/src/sourceediting";
import GeneralHtmlSupportPlugin from "@ckeditor/ckeditor5-html-support/src/generalhtmlsupport";

export default class ClassicEditor extends ClassicEditorBase {}

ClassicEditor.builtinPlugins = [
  EssentialsPlugin,
  GeneralHtmlSupportPlugin,
  AutoformatPlugin,
  BoldPlugin,
  ItalicPlugin,
  ParagraphPlugin,
  HeadingPlugin,
  BlockQuotePlugin,
  ListPlugin,
  AlignmentPlugin,
  ImagePlugin,
  AutoImagePlugin,
  ImageInsertPlugin,
  ImageCaptionPlugin,
  ImageResizePlugin,
  ImageToolbarPlugin,
  LinkPlugin,
  LinkImagePlugin,
  RemoveFormatPlugin,
  SourceEditingPlugin,
];

ClassicEditor.defaultConfig = {
  language: "fr",
  toolbar: {
    items: [
      "heading",
      "bulletedList",
      "numberedList",
      "blockQuote",
      "|",
      "bold",
      "italic",
      "link",
      "alignment:left",
      "alignment:center",
      // INLINE_STYLES: ['cite']
      "|",
      "imageInsert",
      //"insertTable",
      "mediaEmbed",
      "|",
      "undo",
      "redo",
      "|",
      "removeFormat",
      "sourceEditing",
    ],
  },
  heading: {
    options: [
      { model: "paragraph", view: "p", title: "Paragraphe" },
      { model: "heading2", view: "h2", title: "Titre 2" },
      { model: "heading3", view: "h3", title: "Titre 3" },
    ],
  },
  htmlSupport: {
    allow: [
      // Allow keeping the <cite> element from existing content,
      // and inserting it in Source Editing mode, but we don't have
      // a UI for inserting this element in content yet.
      { name: "cite" },
    ],
    // disallow: []
  },
  alignment: {
    options: ["left", "center"],
  },
  image: {
    toolbar: [
      //"imageStyle:inline",
      //"imageStyle:block",
      //"imageStyle:side",
      "imageResize",
      "|",
      "toggleImageCaption",
      "imageTextAlternative",
    ],
    resizeUnit: "px",
    resizeOptions: [
      {
        name: "resizeImage:original",
        value: null,
        label: "Original",
      },
      {
        name: "resizeImage:600",
        value: "600",
        label: "600",
      },
      {
        name: "resizeImage:400",
        value: "400",
        label: "400",
      },
      {
        name: "resizeImage:240",
        value: "240",
        label: "240",
      },
    ],
  },
  mediaEmbed: false,
};
