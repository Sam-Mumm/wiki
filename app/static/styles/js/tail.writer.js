/*
 |  tail.writer - A small GitHub Flavored Markdown editor, written in vanillaJS!
 |  @author     SamBrishes@pytesNET
 |  @version    0.3.2 - Alpha
 |
 |  @license    X11 / MIT License
 |  @copyright  Copyright © 2015 - 2018 SamBrishes, pytesNET <pytes@gmx.net>
 */
;(function(window){
    "use strict";
    var w = window, d = window.document;

    /*
     |  HELPER METHODs
     */
    var tail = {
        hasClass: function(element, classname){
            var regex = new RegExp("(|\s+)" + classname + "(\s+|)");
            return regex.test(element.className);
        },
        addClass: function(element, classname){
            if(!this.hasClass(element, classname)){
                element.className = (element.className.trim() + " " + classname.trim()).trim();
            }
            return element;
        },
        removeClass: function(element, classname){
            var regex = new RegExp("(|\s+)(" + classname + ")(\s+|)");
            if(regex.test(element.className)){
                element.className = (element.className.replace(regex, "$1$3")).trim();
            }
            return element;
        },
        position: function(element, absolute){
            var position = {
                top:    element.offsetTop    || 0,
                left:   element.offsetLeft   || 0,
                width:  element.offsetWidth  || 0,
                height: element.offsetHeight || 0
            };
            if(absolute){
                while(element = element.offsetParent){
                    position.top  += element.offsetTop;
                    position.left += element.offsetLeft;
                }
            }
            return position;
        },
        trigger: function(element, event, options){
            if(CustomEvent && typeof(CustomEvent) !== "undefined"){
                var e = new CustomEvent(event, options);
                return element.dispatchEvent(e);
            }
            var e = d.createEvent("CustomEvent");
            e.initCustomEvent(event, ((options.bubbles)? true: false), ((options.cancelable)? true: false), options.detail);
            return element.dispatchEvent(e);
        },
        clone: function(object, replace){
            replace = (typeof(replace) == "object")? replace: {};
            var clone = object.constructor();
            for(var key in object){
                if(replace.hasOwnProperty(key)){
                    clone[key] = replace[key];
                } else if(object.hasOwnProperty(key)){
                    clone[key] = object[key];
                }
            }
            return clone;
        },
        animate: function(element, callback, delay, prevent){
            if(element.hasAttribute("data-tail-animation")){
                if(!prevent){
                    return;
                }
                clearInterval(tail.animation[element.getAttribute("data-tail-animation")]);
            }
            element.setAttribute("data-tail-animation", "tail-" + ++this.animationCounter);
            this.animation["tail-" + this.animationCounter] = setInterval(function(e, func, tail){
                var animationID = e.getAttribute("data-tail-animation");
                if(func(e) == false){
                    clearInterval(tail.animation[animationID]);
                    if(e.parentElement){
                        e.removeAttribute("data-tail-animation");
                    }
                }
            }, delay, element, callback, this);
        },
        animation: {},
        animationCounter: 0
    };
    tail.IE = (w.navigator.userAgent.indexOf("MSIE") > -1 || w.navigator.userAgent.indexOf("Edge") > -1);

    /*
     |  CONSTRUCTOR
     |  @since  0.2.0
     |  @update 0.3.2
     */
    var tailWriter = function(element, config){
        if(typeof(element) == "string"){
            element = d.querySelectorAll(element);
        }
        if(element instanceof NodeList || element instanceof HTMLCollection){
            if(element.length == 0){
                return false;
            }
            var _return = new Array();
            for(var i = 0; i < element.length; i++){
                _return.push(new tailWriter(element[i], config));
            }
            return _return;
        }
        if(typeof(this) == "undefined"){
            return new tailWriter(element, config);
        }

        // Check Element
        if(!(element instanceof Element)){
            return false;
        }
        if(element.hasAttribute("data-writer") && tailWriter.instances[element.getAttribute(element, "data-writer")]){
            return tailWriter.instances[element.getAttribute("data-writer")];
        }

        // IE Fallback
        config = (typeof(config) == "object")? config: {};
        config.animate = (tail.IE)? false: (config.animate || tailWriter.defaults.animate);

        // Set Instance Data
        this.e = {
            "container": "",
            "editor": element,
            "toolbar": "",
            "statusbar": ""
        };
        this.id = ++tailWriter.counter;
        if(Object.assign){
            this.con = Object.assign({}, tailWriter.defaults, config);
        } else {
            this.con = tail.clone(tailWriter.defaults, config);
        }

        // Build and Return
        tailWriter.instances[this.id] = this.build();
        return this;
    }
    tailWriter.status = "alpha";
    tailWriter.version = "0.3.1";

    // Instances
    tailWriter.counter = 0;
    tailWriter.instances = {};
    tailWriter.placeholder = ("placeholder" in d.createElement("input"));

    /*
     |  STORE :: DEFAULT OPTIONS
     */
    tailWriter.defaults = {
        width: "100%",
        height: ["200px", "500px"],
        classes: "",
        resize: true,
        indentTab: false,
        indentSize: 4,
        toolbar: [
            "headers", "|", "bold", "italic", "strikethrough", "|", "quote", "code",
            "codeblock", "indent", "outdent", "|", "link", "image", "table", "hr", "|",
            "list:unordered", "list:ordered", "|", "preview"
        ],
        toolbarPosition: "top",
        tooltip: "top",
        statusbar: true,
        animate: true
    };

    /*
     |  STORE :: ACTIONs
     */
    tailWriter.actions = {
        bold: {
            syntax: "**$1**",
            callback: "inline"
        },
        italic: {
            syntax: "_$1_",
            callback: "inline"
        },
        underline: {
            syntax: "<u>$1</u>",
            callback: "inline"
        },
        strikethrough: {
            syntax: "~~$1~~",
            callback: "inline"
        },
        code: {
            syntax: "`$1`",
            callback: "inline"
        },
        hr: {
            syntax: "----------",
            callback: "block",
            filter: function(before, content, after){
                if(before.length != before.lastIndexOf("\n")+1){
                    content = "\n" + content;
                }
                if(after.indexOf("\n") < 0 && content.indexOf("\n") <= 0){
                    content = content + "\n";
                }
                return content;
            }
        },
        codeblock: {
            syntax: "```\n$1\n```",
            callback: "inline",
            filter: function(before, content, after, selection){
                if(content == this.syntax.replace("$1", "")){
                    return content;
                }
                content = content.replace(/```\n\n```/g, "");
                selection.start += this.syntax.indexOf("$1");
                selection.end    = content.length - this.syntax.indexOf("$1");
                return content;
            }
        },
        quote: {
            syntax: ">\t$1",
            callback: "block",
            walker: true
        },
        indent: {
            syntax: "\t$1",
            callback: function(markup, action, type){
                var sel = this.selection(), self = this,
                    __1 = this.val.slice(0, sel.start),
                    __2 = this.val.slice(sel.start, sel.end),
                    __3 = this.val.slice(sel.end);

                this.indent = this.indenter(this.lines.current, "count") + 1;
                if(__2.indexOf("\n") == -1){
                    return this.writeLine(this.indenter("\t", "create"), "before");
                }
                __2 = __2.replace(/[^|\n].*/g, function(str){
                    return self.indenter("\t", "create") + str;
                });
                sel.end = __1.length + __2.length;
                return this.write(__1 + __2 + __3, sel);
            }
        },
        outdent: {
            syntax: false,
            callback: function(markup, action, type){
                var sel = this.selection(),
                    __1 = this.val.slice(0, sel.start),
                    __2 = this.val.slice(sel.start, sel.end),
                    __3 = this.val.slice(sel.end, this.val.length),
                    ind = this.indenter("\t"),
                    rep = new RegExp("\n" + ind, "g");

                // Remove Indent
                if(/\n/.test(__2)){
                    __2 = __2.replace(rep, "\n", __2);
                } else if(this.lines.current.indexOf(ind) == 0){
                    var __4 = __1.slice(0, __1.lastIndexOf("\n")+1),
                        __5 = __1.slice(__1.lastIndexOf("\n")+1+ind.length, __1.length);
                    __1 = __4 + __5;
                }
                if(__2.indexOf(ind) == 0){
                    __2 = __2.slice(ind.length);
                }

                sel.start = __1.length;
                sel.end   = __1.length + __2.length;
                return this.write(__1 + __2 + __3, sel);
            }
        },
        header: {
            syntax: function(num){
                num = (num >= 1 && num <= 6)? parseInt(num): 1;
                return (new Array(num + 1).join("#")) + " $1";
            },
            callback: "block",
            filter: function(before, content, after, selection){
                if(content == "\n==========" || content == "\n----------"){
                    selection.start = selection.end = before.length;
                }
                return content;
            }
        },
        list: {
            title: function(type){
                var type = (typeof(type) == "undefined")? "unordered": type;
                return "list" + type[0].toUpperCase() + type.slice(1);
            },
            syntax: function(type){
                switch(type){
                    case "checked":
                        return "- [x]\t$1";
                    case "unchecked":
                        return "- [ ]\t$1";
                    case "ordered":
                        return "1.\t$1";
                }
                return "-\t$1";
            },
            filter: function(before, content, after){
                if(content.indexOf("1.") !== 0){
                    return content;
                }
                var number = before.match(/^([0-9]+)\.\s+/gm);
                if(number){ return content.replace("1", (number.length+1).toString()); }
                return content;
            },
            callback: "block",
            walker: true
        },
        headers: {
            syntax: self.header,
            callback: function(markup, action, type, args){
                var content = '<form>';
                for(var i = 1; i <= ((args.length > 0 && args[0] == "x3")? 3: 6); i++){
                    content += '<div class="tail-writer-item tail-writer-item-header-' + i + '">' +
                        '   <button onclick="this.parentElement.parentElement.querySelector(\'input\').value = ' + i + ';">' +
                        '       <span class="icon-header-' + i + '" ></span> Header ' + i +
                        '   </button>' +
                        '</div>';
                }
                content += '<input type="hidden" name="header" value="" /></form>';
                this.showDropdown(type + ((args.length > 0)? "-" + args.join("-"): ""), content, function(form, event){
                    var num = parseInt(form.header.value);
                    this.perform("header", [((num < 1 || num > 6 || isNaN(num))? 1: num)]);
                    return true;
                });
            }
        },
        link: {
            syntax: "[$1](url)",
            callback: function(markup, action, type, args){
                if(args.length == 0){
                    return this.do_inline(markup, action, type);
                }
                var content = '' +
                    '<form>' +
                    '   <div class="tail-writer-row">' +
                    '       <span class="tail-writer-label tail-writer-label-title">' + __(type + "Title") + '</span>' +
                    '       <input type="text" name="title" value="" class="field-text" placeholder="' + __(type + "Title") + '" />' +
                    '   </div>' +
                    '   <div class="tail-writer-row">' +
                    '       <span class="tail-writer-label tail-writer-label-url">' + __(type + "URL") + '</span>' +
                    '       <input type="text" name="url" value="" class="field-text" placeholder="' + __(type + "URL") + '" />' +
                    '   </div>' +
                    '   <div>' +
                    '       <button name="type" value="' + type + '">' +  __(type + "Create") + '</button>' +
                    '   </div>' +
                    '</form>', self = this,
                    handle = function(form){
                        var markup = tailWriter.actions[form.type.value].syntax + " ";
                            markup = markup.replace("url", form.url.value).replace("$1", form.title.value);
                        self.do_inline(markup, self, type);
                        return true;
                    };
                if(args[0] == "dropdown"){
                    this.showDropdown(type + "-dropdown", content, handle);
                } else {
                    this.showDialog(type + "-dialog", content, handle);
                }
            },
            filter: function(before, content, after, selection){
                if(content == "[](url)"){
                    selection.end += "link-title".length;
                    return "[link-title](url)";
                }
                return content;
            }
        },
        image: {
            syntax: "![$1](url)",
            callback: function(markup, action, type, args){
                tailWriter.actions.link.callback.call(this, markup, action, type, args);
            },
            filter: function(before, content, after, selection){
                if(content == "![](url)"){
                    selection.end += "image-title".length;
                    return "![image-title](url)";
                }
                return content;
            }
        },
        table: {
            syntax: false,
            callback: function(markup, action, type, args){
                var content = '' +
                    '<form>' +
                    '   <div class="tail-writer-row">' +
                    '       <span class="tail-writer-label tail-writer-label-rows">' + __("tableRows") + '</span>' +
                    '       <input type="number" name="rows" value="3" class="field-number" placeholder="' + __("tableRows") + '" />' +
                    '   </div>' +
                    '   <div class="tail-writer-row">' +
                    '       <span class="tail-writer-label tail-writer-label-cols">' + __("tableCols") + '</span>' +
                    '       <input type="number" name="cols" value="3" class="field-number" placeholder="' + __("tableCols") + '" />' +
                    '   </div>' +
                    '   <div class="tail-writer-row">' +
                    '       <input type="checkbox" id="tail-writer-table-head-' + this.id + '" name="head" value="1" class="field-header" />' +
                    '       <label for="tail-writer-table-head-' + this.id + '">' + __("tableHead") + '</label>' +
                    '   </div>' +
                    '   <div>' +
                    '       <button>' +  __("tableCreate") + '</button>' +
                    '   </div>' +
                    '</form>', self = this,
                    handle = function(form){
                        var head = form.head.checked,
                            rows = parseInt(form.rows.value), cols = parseInt(form.cols.value);
                            rows = isNaN(rows)? 3: rows;      cols = isNaN(cols)? 3: cols;

                        var content = '', spaces = 12;
                        for(var i = 0; i <= rows; i++){
                            if(!head && i == 0){
                                continue; // Skip Table Header
                            }

                            for(var i2 = 1; i2 <= cols; i2++){
                                content += "| ";
                                for(var s = 0; s < spaces; s++){
                                    content += " ";
                                }
                                content += " ";
                            }
                            content += "|\n";

                            if(i == 0){
                                for(var i2 = 1; i2 <= cols; i2++){
                                    content += "| ";
                                    for(var s = 0; s < spaces; s++){
                                        content += "-";
                                    }
                                    content += " ";
                                }
                                content += "|\n";
                            }
                        }
                        this.do_block(content, self, "table");
                        return true;
                    };
                if(args[0] == "dropdown"){
                    this.showDropdown(type + "-dropdown", content, handle);
                } else {
                    this.showDialog(type + "-dialog", content, handle);
                }
            }
        }
    };
    if(typeof(marked) != "undefined"){
        tailWriter.actions.preview = {
            syntax: false,
            callback: function(markup, action, type){
                if(!tail.hasClass(this.current, "active")){
                    var content = this.e.editor.value;
                    if(content.length == 0){
                        content = __("previewEmpty");
                    }

                    // Render Content and Preview
                    var preview = d.createElement("DIV");
                        preview.innerHTML = tailWriter.parse(content);
                        preview.className = "tail-writer-preview";
                        preview.style.width = this.e.editor.outerWidth;
                        preview.style.height = this.e.editor.outerHeight;

                    // Manipulate Elements
                    tail.removeClass(this.current, "icon-preview");
                    tail.addClass(this.current, "active icon-editor");
                    tail.addClass(this.e.container, "tail-writer-preview");
                    this.current.setAttribute("data-writer-title", __("previewExit"));

                    this.e.editor.style.display = "none";
                    this.e.container.insertBefore(preview, this.e.editor);

                    var tools = this.e.toolbar.querySelectorAll("button:not(.icon-editor)");
                    for(var i = 0; i < tools.length; i++){
                        tail.addClass(tools[i], "disabled");
                    }
                } else {
                    tail.removeClass(this.current, "active icon-editor");
                    tail.removeClass(this.e.container, "tail-writer-preview");
                    tail.addClass(this.current, "icon-preview");
                    this.current.setAttribute("data-writer-title", __("preview"));

                    this.e.container.removeChild(this.e.container.querySelector(".tail-writer-preview"));
                    this.e.editor.style.display = "block";

                    var tools = this.e.toolbar.querySelectorAll("button.disabled");
                    for(var i = 0; i < tools.length; i++){
                        tail.removeClass(tools[i], "disabled");
                    }
                }

                if(MouseEvent && MouseEvent.name){
                    var ev = new MouseEvent("mouseout");
                    this.current.dispatchEvent(ev);
                    setTimeout(function(element){
                        var ev = new MouseEvent("mouseover");
                        element.dispatchEvent(ev);
                    }, 200, this.current);
                } else if(d.createEvent){ /* Fallback */
                    var ev = d.createEvent("MouseEvent");
                        ev.initEvent("mouseout", true, false, {});
                    this.current.dispatchEvent(ev);
                    (function(element){
                        setTimeout(function(){
                            var ev = d.createEvent("MouseEvent");
                                ev.initEvent("mouseover", true, false, {});
                            element.dispatchEvent(ev);
                        }, 200);
                    })(this.current);
                }
            }
        };
    }
    var _action = function(type, args){
        if(typeof(type) == "string" && tailWriter.actions.hasOwnProperty(type)){
            var action = tailWriter.actions[type];
        } else {
            return false;
        }

        // Handle Syntax
        if(typeof(action.syntax) == "function"){
            action.markup = action.syntax.apply(action, args);
        } else {
            action.markup = action.syntax;
        }

        // Handle Title
        action.id = type + ((args.length > 0)? "-" + args.join("-"): "");
        if(typeof(action.title) == "function"){
            action.string = __(action.title.apply(action, args));
        } else {
            action.string = __(type);
        }
        return action;
    };
    var _filter = function(action, before, content, after, selection){
        if(typeof(action.filter) == "function"){
            return action.filter.call(action, before, content, after, selection);
        }
        return content;
    };

    /*
     |  STORE :: STRINGS
     */
    tailWriter.strings = {
        bold: "Bold",
        italic: "Italic",
        underline: "Underline",
        strikethrough: "Strikethrough",
        code: "Inline Code",
        link: "Link",
        image: "Image",
        hr: "Horizontal Rule",
        quote: "Blockquote",
        indent: "Indent",
        outdent: "Outdent",
        header: "Header",
        codeblock: "Code Block",
        listOrdered: "Ordered List",
        listUnordered: "Unordered List",
        listChecked: "Checked List",
        listUnchecked: "Unchecked List",
        headers: "Headers",
        table: "Table",
        tableRows: "Rows",
        tableCols: "Columns",
        tableHead: "Include Header",
        tableCreate: "Create Table",
        linkDialog: "Link (Dialog)",
        imageDialog: "Image (Dialog)",
        tableDialog: "Table (Dialog)",
        linkTitle: "Link Title",
        linkURL: "Link URL",
        linkCreate: "Add Link",
        imageTitle: "Image Title",
        imageURL: "Image URL",
        imageCreate: "Add Image",
        lineCounter: "Lines",
        charCounter: "Characters",
        wordCounter: "Words"
    };
    if(typeof(marked) != "undefined"){
        tailWriter.strings.preview = "Preview";
        tailWriter.strings.previewEmpty = "Nothing to preview yet!";
        tailWriter.strings.previewExit = "Exit Preview Mode";
    }
    var __ = function(key){
        if(tailWriter.strings.hasOwnProperty(key)){
            return tailWriter.strings[key];
        }
        return key;
    };

    /*
     |  API :: MARKDOWN PARSER
     |  @since  0.3.0
     |  @update 0.3.0
     */
    tailWriter.parse = function(content){
        if(typeof(marked) == "undefined"){
            return content;
        }

        // Checklist Support (https://github.com/chjj/marked/issues/107#issuecomment-44542001)
        var render = new marked.Renderer();
        render.listitem = function(text){
            if(/^\s*\[[x ]\]\s*/.test(text)){
                text = text
                    .replace(/^\s*\[ \]\s*/, '<input type="checkbox"> ')
                    .replace(/^\s*\[x\]\s*/, '<input type="checkbox" checked> ');
                return '<li style="list-style: none">' + text + '</li>';
            }
            return '<li>' + text + '</li>';
        };
        return marked(content, {renderer: render});
    };

    /*
     |  API :: EXTEND ACTION BUTTON
     |  @since  0.2.0
     |  @update 0.3.0
     */
    tailWriter.extend = function(type, action, strings){
        if(tailWriter.actions.hasOwnProperty(type)){
            return false;
        }
        if(typeof(action) != "object" || typeof(strings) != "object"){
            return false;
        }

        // Add Action and Strings
        tailWriter.actions[type] = action;
        tailWriter.strings = Object.assign(tailWriter.strings, strings);
        return true;
    };

    /*
     |  METHODS
     */
    tailWriter.prototype = {
        e: {},              // Elements
        id: 0,              // Unique ID
        con: {},            // Configuration

        val: "",            // Current Value
        walk: false,        // Walker
        lines: {},          // Lines
        indent: 0,          // Current Indent Size
        current: 0,         // Current Action
        dialogs: [],        // Current Dialogs
        dropdowns: [],      // Current Dropdowns

        /*
         |  INSTANCE :: BUILD EDITOR
         |  @since  0.2.0
         |  @update 0.3.0
         */
        build: function(){
            var self = this; this.read();

            // Editor Container
            this.e.container = d.createElement("div");
            this.e.container.className = "tail-writer-object " + this.con.classes;
            this.e.container.style.width = this.con.width;
            this.e.container.setAttribute("tail-writer-object", this.id);

            var parent = this.e.editor.parentElement;
            this.e.container.appendChild(this.e.editor);
            parent.appendChild(this.e.container);

            // Create Toolbar
            this.e.toolbar = d.createElement("div");
            this.e.toolbar.className = "tail-writer-toolbar tail-writer-toolbar-" + this.con.toolbarPosition;
            this.e.toolbar.setAttribute("data-writer-toolbar", this.con.toolbarPosition);
            this.e.container.insertBefore(this.e.toolbar, this.e.editor)

            for(var i = 0; i < this.con.toolbar.length; i++){
                var type   = this.con.toolbar[i].split(":"),
                    args   = (type.length > 1? type[1].split(","): []),
                    action = _action(type[0], args);

                if(type[0] !== "|" && action == false){
                    continue;
                }

                // Create Action
                if(type[0] === "|"){
                    var button = d.createElement("span");
                        button.className = "tail-writer-sep";
                } else {
                    var button = d.createElement("button");
                        button.className = "tail-writer-button icon-" + action.id;
                        button.className = "tail-writer-button icon-" + action.id;
                        button.setAttribute("data-writer-title", action.string);
                        button.setAttribute("data-writer-action", type[0] + ((args.length > 0)? "-" + args.join("-"): ""));
                    button.addEventListener("click", function(event){
                        event.preventDefault();

                        if(tail.hasClass(event.target, "tail-writer-button")){
                            var removed = self.hideDropdown.call(self);
                            if(removed.indexOf(this.getAttribute("data-writer-action") == -1)){
                                var args = this.getAttribute("data-writer-action").split("-");
                                self.current = this;
                                self.perform.call(self, args.shift(), args);
                            }
                        }
                    });

                    // Add Tooltip
                    if(this.con.tooltip !== false){
                        button.addEventListener("mouseover", function(event){
                            self.tooltip.call(self, event, this);
                        });
                        button.addEventListener("mouseout", function(event){
                            self.tooltip.call(self, event, this);
                        });
                    }
                }
                this.e.toolbar.appendChild(button);
            };

            // Create Statusbar
            if(this.con.statusbar){
                this.e.statusbar = d.createElement("div");
                this.e.statusbar.className = "tail-writer-statusbar";
                this.e.statusbar.innerHTML = '' +
                    '<div class="tail-writer-lines">' + __("lineCounter") + ': <span class="tail-writer-count"></span></div>' +
                    '<div class="tail-writer-chars">' + __("charCounter") + ': <span class="tail-writer-count"></span></div>' +
                    '<div class="tail-writer-words">' + __("wordCounter") + ': <span class="tail-writer-count"></span></div>';
                this.e.container.appendChild(this.e.statusbar);
                this.statusbar();
            }

            // Editor Field
            this.e.editor.setAttribute("data-writer-editor", this.id);
            if(!isNaN(parseInt(this.con.height[0]))){
                var height = parseInt(this.con.height[0]);
            } else {
                var height = parseInt(this.e.container.outerHeight);
                if(height < 200){
                    height = 200;
                }
            }
            this.e.editor.style.width = parseInt(this.con.width) + "%";
            this.e.editor.style.height = height + "px";
            this.e.editor.style.minHeight = height + "px";
            if(!isNaN(parseInt(this.con.height[1]))){
                this.e.editor.style.maxHeight = parseInt(this.con.height[1]) + "px";
            }
            if(this.con.indent){
                this.e.editor.style.tabSize = this.con.indentSize;
            }
            this.e.editor.className += " tail-writer-editor";

            // Event Handling
            var events = ["click", "input", "change", "keydown", "keyup"];
            for(var i = 0; i < events.length; i++){
                this.e.editor.addEventListener(events[i], function(event){
                    self.handle.call(self, event);
                });
            }

            if(this.con.resize){
                this.resize(false);
            }
            return this;
        },

        /*
         |  HANDLE :: EDITOR
         |  @since  0.2.0
         |  @update 0.3.1
         */
        handle: function(event){
            var self = this; this.read();

            // On Click
            if(event.type == "click"){
                this.hideDropdown.call(this);
            }

            // Listen for Keys
            if(event.type === "keydown"){

                // CTRL + X (Cut Line)
                if(event.ctrlKey && event.keyCode == 88){
                    event.preventDefault();

                    var sel = this.selection();
                    if(sel.start == sel.end){
                        var linestart = -1, lineend = sel.end;
                        while(sel.start > -1){
                            linestart = (sel.start > 0)? this.val.indexOf("\n", sel.start--): 0;
                            if(sel.start < 0 || (linestart > -1 && linestart < lineend)){
                                sel.start = linestart;
                                sel.end   = linestart + this.lines.current.length + 1;
                                break;
                            }
                        }
                    }
                    //@todo Clipboard Binding
                    this.write(this.val.slice(0, sel.start) + this.val.slice(sel.end));
                    this.selection(sel.start+1, sel.start+1);
                    return false;
                }

                // CTRL + D (Duplicate Line)
                if(event.ctrlKey && event.keyCode == 68){
                    event.preventDefault();
                    return this.writeLine("\n" + this.lines.current, "after");
                }

                // Tab
                if(event.keyCode == 9){
                    event.preventDefault();
                    if(event.shiftKey){
                        return this.perform("outdent", []);
                    } else {
                        return this.perform("indent", []);
                    }
                }

                // Enter
                if(event.keyCode == 13){
                    if(this.walkable(this.lines.current)){
                        event.preventDefault();
                        this.writeLine(this.indenter("", "create"));
                        return this.perform(this.walk[0], this.walk[1]);
                    }
                    return true;
                }
            }

            // Modify Content
            if(this.con.resize){
                this.resize(true);
            }
            if(this.con.statusbar){
                this.statusbar();
            }
        },

        /*
         |  HANDLE :: CHECK FOR AN WALKABLE CONTINUE
         |  @since  0.2.0
         |  @update 0.3.0
         */
        walkable: function(string){
            if(!this.walk || string == undefined){
                this.walk = false;
                return false;
            }
            var action = _action(this.walk[0], this.walk[1]),
                syntax = this.indenter(action.markup.replace("$1", ""));

            // Check Lines
            if(string.indexOf(syntax) < 0){
                this.walk = false;
                return false;
            }
            if(string == syntax){
                this.writeLine("", "replace");
                this.walk = false;
                return false;
            }
            return true;
        },

        /*
         |  HANDLE :: TOOLTIPs
         |  @since  0.2.0
         |  @update 0.3.2
         */
        tooltip: function(event, element){
            if(this.con.tooltip == false){
                return false;
            }
            var offset  = tail.position(event.target),
                classes = "tail-writer-tooltip-" + event.target.getAttribute("data-writer-action");

            if(!tail.hasClass(event.target.parentElement, "tail-writer-toolbar")){
                return false;
            }
            if(event.type == "mouseover"){
                if(tail.hasClass(event.target, "disabled")){
                    return;
                }
                if(this.e.container.querySelectorAll("." + classes).length == 0){
                    var tooltip = d.createElement("DIV");
                        tooltip.innerText = __(event.target.getAttribute("data-writer-title"));
                        tooltip.className = "tail-writer-tooltip tail-writer-tooltip-" + this.con.tooltip + " " + classes;
                        tooltip.style.opacity = 0;
                        tooltip.style.position = "absolute";
                    this.e.container.insertBefore(tooltip, this.e.container.children[0]);

                    // Calc Position
                    var style = w.getComputedStyle(this.e.toolbar);
                    if(this.con.tooltip == "bottom"){
                        tooltip.style.top = (parseInt(style.top) + offset.height + tooltip.offsetHeight) + "px";
                    } else {
                        tooltip.style.top = "-2px";
                    }
                    tooltip.style.left = (parseInt(style.left) + offset.left + (offset.width/2) - (tooltip.offsetWidth/2)) + "px";

                    // Animate
                    if(this.con.animate){
                        tail.animate(tooltip, function(element){
                            if(parseFloat(element.style.opacity) < 1.0){
                                element.style.opacity = parseFloat(element.style.opacity) + 0.1;
                                return true;
                            }
                            return false;
                        }, 10, true);
                    } else {
                        tooltip.style.opacity = 1;
                    }
                }
            } else {
                var element = this.e.container.querySelector("." + classes);
                if(element && this.con.animate){
                    tail.animate(element, function(element){
                        if(parseFloat(element.style.opacity) > 0.0){
                            element.style.opacity = parseFloat(element.style.opacity) - 0.1;
                            return true;
                        }
                        if(element.parentElement){
                            element.parentElement.removeChild(element);
                        }
                        return false;
                    }, 10, true);
                } else if(element){
                    if(element.parentElement){
                        element.parentElement.removeChild(element);
                    }
                }
            }
        },

        /*
         |  HANDLE :: RESIZE
         |  @since  0.2.0
         |  @update 0.3.2
         */
        resize: function(scroll){
            var clone   = this.e.editor.cloneNode(),
                style   = w.getComputedStyle(this.e.editor),
                padding = parseInt(style.paddingTop) + parseInt(style.paddingBottom);

            // Clone Element
            clone.style.height = "auto";
            clone.style.minHeight = "none";
            clone.style.maxHeight = "none";
            clone.style.opacity = 0;
            clone.style.position = "position";
            clone.value = this.val;
            this.e.container.insertBefore(clone, this.e.editor);

            // Get Data
            var _toTop = clone.scrollTop,
                height = clone.scrollHeight;
            this.e.container.removeChild(clone, clone.selectionStart);

            // Compare
            this.e.editor.style.height = (height - padding) + "px";
            if(scroll == true && this.e.editor.value.length - this.selection().start <= 3){
                this.e.editor.scrollTop = (height - padding);
            }
        },

        /*
         |  HANDLE :: STATUSBAR
         |  @since  0.2.0
         |  @update 0.3.0
         */
        statusbar: function(action){
            var data = {
                chars: (this.val.length).toString(),
                lines: (this.val.match(/^|\n/g) || [""]).length.toString(),
                words: "0".toString()
            };

            // Count Words
            var words = this.val.trim().replace(/[\n\t\.]/g, " ").trim();
                words = words.replace(/[^a-zA-Z0-9 ]/g, "").replace(/\s\s+/g, " ").split(" ");
            if(words.length <= 1 && words[0].length == 0){
                data.words =  0;
            } else {
                data.words = words.length;
            }

            // Count Selected
            var sel = this.selection();
            if(sel.start !== sel.end){
                var __2   = this.val.slice(sel.start, sel.end);
                    words = __2.trim().replace(/[\n\t\.]/g, " ").trim();
                    words = words.replace(/[^a-zA-Z0-9 ]/g, "").replace(/\s\s+/g, " ").split(" ");

                data.chars = '<span class="current">' + __2.length + ' / </span>' + data.chars;
                data.lines = '<span class="current">' + (__2.match(/^|\n/g) || [""]).length + ' / </span>' + data.lines;
                if(words.length <= 1 && words[0].length == 0){
                    data.words = '<span class="current">0 / </span>' + data.words;
                } else {
                    data.words = '<span class="current">' + words.length + ' / </span>' + data.words;
                }
            }

            // Inject
            this.e.statusbar.querySelector(".tail-writer-lines span").innerHTML = data.lines;
            this.e.statusbar.querySelector(".tail-writer-chars span").innerHTML = data.chars;
            this.e.statusbar.querySelector(".tail-writer-words span").innerHTML = data.words;
        },

        /*
         |  HELPER :: (G|S)ET SELECTION
         |  @since  0.2.0
         |  @update 0.3.0
         */
        selection: function(start, end){
            if(start == undefined){
                return {start: this.e.editor.selectionStart, end: this.e.editor.selectionEnd};
            } else if(typeof(start) !== "number"){
                start = this.val.length;
            }
            if(end == undefined){
                end = start;
            }
            this.e.editor.focus();
            this.e.editor.selectionStart = start;
            this.e.editor.selectionEnd = end;
            return true;
        },

        /*
         |  HELPER :: INDENTER
         |  @since  0.2.0
         |  @update 0.3.0
         */
        indenter: function(string, action){
            if(this.con.indentTab){
                var indent = "\t";
            } else {
                var indent = Array(this.con.indentSize + 1).join(" ");
            }

            // Count
            if(action === "count"){
                var temp = string.replace(".", ""),
                    rexp = new RegExp(indent, "gi");
                    temp = temp.replace(rexp, ".").split(/([^\.])/);
                if(typeof(temp) == "object" && temp.length > 0){
                    return temp[0].length;
                }
                return 0;
            }

            // Create
            if(action === "create"){
                var lines = string.split("\n");
                for(var i = 0; i < lines.length; i++){
                    if(i === 0){
                        continue;
                    }
                    lines[i] = Array((this.indent + 1)).join("\t") + lines[i];
                }
                string = lines.join("\n");
            }

            // Replace
            if(!this.con.indentTab){
                string = string.replace(/\t/g, indent);
            }
            return string;
        },

        /*
         |  CORE :: READ CONTENT
         |  @since  0.2.0
         |  @update 0.3.0
         */
        read: function(){
            this.val = this.indenter(this.e.editor.value);

            // Split Content
            var sel = this.selection(),
                __p = this.val.slice(0, sel.start).split("\n"),
                __n = this.val.slice(sel.start, this.val.length).split("\n");

            // Get Lines
            this.lines = {
                "current":    __p.pop() + __n.shift(),
                "previous":    (__p.length > 0)? __p.pop(): undefined,
                "next":        (__n.length > 0)? __n.shift(): undefined,
            };
            this.indent = this.indenter(this.lines.current, "count");
        },

        /*
         |  CORE :: WRITE CONTENT
         |  @since  0.2.0
         |  @update 0.3.0
         */
        write: function(content, selection){
            this.e.editor.value = content;
            if(typeof(selection) == "object"){
                this.selection(selection.start, selection.end);
            }
            this.read();
        },

        /*
         |  CORE :: WRITE LINE
         |  @since  0.2.0
         |  @update 0.3.0
         */
        writeLine: function(line, handle){
            var sel = this.selection(),
                __p = this.val.slice(0, sel.start).split("\n"),
                __n = this.val.slice(sel.start, this.val.length).split("\n"),
                __c = __p.pop() + __n.shift();

                __p = ((__p.length > 0)? __p.join("\n") + "\n": "");
                __n = ((__n.length > 0)? "\n" + __n.join("\n"): "");

            if(handle == "replace"){
                this.e.editor.value = __p + line + __n;
                this.selection(__p.length + line.length);
            } else if(handle == "before"){
                this.e.editor.value = __p + line + __c + __n;
                this.selection(__p.length + line.length + __c.split("\n")[0].length);
            } else {
                this.e.editor.value = __p + __c + line + __n;
                this.selection(__p.length + line.length + __c.length);
            }
            this.read();
        },

        /*
         |  CORE :: SHOW DROPDOWN
         |  @since  0.2.0
         |  @update 0.3.2
         */
        showDropdown: function(type, content, callback){
            var self = this;
            if(tail.hasClass(this.current, "disabled")){
                return;
            }

            // Create Dropdown
            var dropdown = d.createElement("DIV");
                dropdown.innerHTML = content;
                dropdown.className = "tail-writer-dropdown tail-writer-dropdown-" + type;
                dropdown.style.opacity = 0;
                dropdown.style.position = "absolute";
            this.e.container.appendChild(dropdown);

            // Format Dropdown
            var position = tail.position(this.current), style = w.getComputedStyle(this.e.toolbar);
            dropdown.style.top = position.top + position.height + "px";
            dropdown.style.left = position.left + parseInt(style.left) + "px";
            dropdown.tailWriter = callback;

            if(this.con.animate){
                tail.animate(dropdown, function(element){
                    if(parseFloat(element.style.opacity) < 1.0){
                        element.style.opacity = parseFloat(element.style.opacity) + 0.1;
                        return true;
                    }
                    return false;
                }, 10, true);
            } else {
                dropdown.style.opacity = 1;
            }

            dropdown.querySelector("form").addEventListener("submit", function(event){
                event.preventDefault();
                if(this.parentElement.tailWriter.call(self, this.elements, event)){
                    self.hideDropdown.call(self);
                }
            });
        },

        /*
         |  CORE :: HIDE DROPDOWN
         |  @since  0.2.0
         |  @update 0.3.2
         */
        hideDropdown: function(){
            var removed = new Array(),
                dropdowns = this.e.container.querySelectorAll(".tail-writer-dropdown");
            if(dropdowns.length > 0){
                for(var i = 0; i < dropdowns.length; i++){
                    removed.push(dropdowns[i].getAttribute("data-writer-dropdown"));

                    if(this.con.animate){
                        tail.animate(dropdowns[i], function(element){
                            if(parseFloat(element.style.opacity) > 0.0){
                                element.style.opacity = parseFloat(element.style.opacity) - 0.1;
                                return true;
                            }
                            element.parentElement.removeChild(element);
                            return false;
                        }, 10, true);
                    } else {
                        dropdowns[i].parentElement.removeChild(dropdowns[i]);
                    }
                }
            }
            return removed;
        },

        /*
         |  CORE :: SHOW DIALOG
         |  @since  0.2.0
         |  @update 0.3.2
         */
        showDialog: function(type, content, callback){
            var self = this;
            if(tail.hasClass(this.current, "disabled")){
                return;
            }

            // Create Mask
            var mask = d.createElement("DIV");
                mask.className = "tail-writer-mask";
                mask.style.top = 0;
                mask.style.left = 0;
                mask.style.right = 0;
                mask.style.bottom = 0;
                mask.style.opacity = 0;
                mask.style.position = "absolute";
            mask.addEventListener("click", function(event){
                self.hideDialog.call(self);
            });
            this.e.container.appendChild(mask);

            if(this.con.animate){
                tail.animate(mask, function(element){
                    if(parseFloat(element.style.opacity) < 1.0){
                        element.style.opacity = parseFloat(element.style.opacity) + 0.1;
                        return true;
                    }
                    return false;
                }, 10, true);
            } else {
                mask.style.opacity = 1;
            }

            // Create Dialog
            var dialog = d.createElement("DIV");
                dialog.innerHTML = content;
                dialog.className = "tail-writer-dialog tail-writer-dialog-" + type;
                dialog.style.display = "block";
                dialog.style.opacity = 0;
                dialog.style.position = "absolute";
            this.e.container.appendChild(dialog);

            // Format Dialog
            dialog.style.top = (this.e.container.offsetHeight / 2 - dialog.offsetHeight / 2) + "px"
            dialog.style.left = (this.e.container.offsetWidth / 2 - dialog.offsetWidth / 2) + "px";
            dialog.tailWriter = callback;

            if(this.con.animate){
                tail.animate(dialog, function(element){
                    if(parseFloat(element.style.opacity) < 1.0){
                        element.style.opacity = parseFloat(element.style.opacity) + 0.1;
                        return true;
                    }
                    return false;
                }, 10, true);
            } else {
                dialog.style.opacity = 1;
            }

            dialog.querySelector("form").addEventListener("submit", function(event){
                event.preventDefault();
                if(this.parentElement.tailWriter.call(self, this.elements, event)){
                    self.hideDialog.call(self);
                }
            });
        },

        /*
         |  CORE :: HIDE DIALOG
         |  @since  0.2.0
         |  @update 0.3.2
         */
        hideDialog: function(){
            var removed = new Array(),
                dialogs = this.e.container.querySelectorAll(".tail-writer-dialog");
            if(dialogs.length > 0){
                for(var i = 0; i < dialogs.length; i++){
                    removed.push(dialogs[i].getAttribute("data-writer-dialog"));

                    if(this.con.animate){
                        tail.animate(dialogs[i], function(element){
                            if(parseFloat(element.style.opacity) > 0.0){
                                element.style.opacity = parseFloat(element.style.opacity) - 0.1;
                                return true;
                            }
                            element.parentElement.removeChild(element);
                            return false;
                        }, 10, true);
                    } else {
                        dialogs[i].parentElement.removeChild(dialogs[i]);
                    }
                }
            }

            // Mask
            var mask = this.e.container.querySelector(".tail-writer-mask");
            if(mask && this.con.animate){
                tail.animate(this.e.container.querySelector(".tail-writer-mask"), function(element){
                    if(parseFloat(element.style.opacity) > 0.0){
                        element.style.opacity = parseFloat(element.style.opacity) - 0.1;
                        return true;
                    }
                    element.parentElement.removeChild(element);
                    return false;
                }, 10, true);
            } else {
                mask.parentElement.removeChild(mask);
            }
            return removed;
        },

        /*
         |  CORE :: REMOVE TAIL.WRITER
         |  @since  0.2.0
         |  @update 0.3.0
         */
        remove: function(){
            this.e.container.removeChild(this.e.toolbar);
            this.e.container.removeChild(this.e.statusbar);

            var textarea = this.e.container.querySelector("textarea");
            textarea.removeAttribute("data-writer-editor");
            tail.removeClass(textarea, "tail-writer-editor");

            this.e.container.parentElement.replaceChild(textarea, this.e.container);
            return true;
        },

        /*
         |  ACTION :: PERFORM TOOLBAR ACTION
         |  @since  0.2.0
         |  @update 0.3.0
         */
        perform: function(type, args){
            var action = _action(type, args);
            if(action === false){
                return false;
            }

            // Call Action
            if(typeof(action.callback) == "function"){
                action.callback.call(this, action.markup, action, type, args);
            } else if(["inline", "block"].indexOf(action.callback) >= 0){
                this["do_" + action.callback].call(this, action.markup, action, type, args);
            }

            // Set Walker
            if(typeof(action.walker) !== "undefined" && action.walker){
                this.walk = [type, args, (this.walk instanceof Array)? this.walk[2]++: 0];
            }
            return false;
        },

        /*
         |  ACTION :: INLINE ACTIONs
         |  @since  0.2.0
         |  @update 0.3.0
         */
        do_inline: function(markup, action, type){
            var sel = this.selection(),
                __1 = this.val.slice(0, sel.start),
                __2 = this.val.slice(sel.start, sel.end),
                __3 = this.val.slice(sel.end, this.val.length);

            // Modify Content
            if(sel.start !== sel.end && __2.indexOf("\n\n") > -1){
                sel.start = __1.length;
                sel.end = __1.length + ((markup.length-2) * ((__2.match(/\n\n/g) || []).length+1)) + __2.length;

                __2 = __2.split("\n\n"); __2.forEach(function(string, i){
                    __2[i] = markup.replace("$1", __2[i]);
                });
                __2 = _filter(action, __1, __2.join("\n\n"), __3, sel);
            } else {
                sel.start = __1.length + markup.indexOf("$1");
                sel.end = __1.length + markup.indexOf("$1") + __2.length;
                __2 = _filter(action, __1, markup.replace("$1", __2), __3, sel);
            }
            this.write(__1 + __2 + __3, sel);
        },

        /*
         |  ACTION :: BLOCK ACTIONs
         |  @since  0.2.0
         |  @update 0.3.0
         */
        do_block: function(markup, action, type){
            var sel = this.selection(),
                __1 = this.val.slice(0, sel.start),
                __2 = this.val.slice(sel.start, sel.end),
                __3 = this.val.slice(sel.end, this.val.length);

            // Modify Content
            if(sel.start !== sel.end){
                var self = this;
                __2 = __2.replace(/[^|\n]([^\n]+)/g, function(string){
                    return self.indenter(markup.replace("$1", string), "create");
                });
                __2 = _filter(action, __1, __2, __3, sel);
            } else {
                if(__1.length > 0 && __1.length > __1.lastIndexOf("\n")+1){
                    __1 += "\n";
                }
                __2 = this.indenter(markup.replace("$1", ""), "create");
                sel.start = sel.end = __1.length + __2.length;
                __2 = _filter(action, __1, __2, __3, sel);
            }
            this.write(__1 + __2 + __3, sel);
        }
    }

    // Assign to jQuery
    if(typeof(jQuery) !== "undefined"){
        jQuery.fn.extend({
            tailWriter: function(options){
                return this.each(function(){
                    return new tailWriter(this, options);
                });
            }
        });
    }

    // Assign to MooTools
    if(typeof(d.id) !== "undefined"){
        Element.implement({
            tailWriter: function(options){
                return new tailWriter(this, options);
            }
        });
    }

    // Assign to Window
    if(typeof(w.tail) == "undefined"){
        w.tail = {};
    }
    w.tail.writer = tailWriter;
    return w.tail.writer;
})(this);
