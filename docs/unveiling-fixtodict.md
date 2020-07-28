Hello!
I would like to unveil a project I've been working on for the last couple of weeks. It's fully open source and you can check it out [here](https://github.com/fixipe/fix2dict/).

When I started working on FIX2dict, I set out to dramatically improve the state of the art for programmatic access to FIX Repository data. This is made possible by adopting the widespread JSON data format, as well as two other popular web standards:

1. JSON Schema.
2. JSON Patch.

FIX Repository has traditionally been released as XML files, but XML itself is most commonly used in legacy systems and **should not**, in my experience, be the reference format for modern standards. It has obviously served us well, but here's a few comparison points with JSON:

* You often need third-party, poorly-supported libraries to work with XML. In recent years (decades, actually), most APIs and tools have switched to less verbose and more ubiquitous data formats.
* JSON is extremely popular and benefits from a huge range of existing tooling.

Hopefully, I have made my case clear for considering the JSON ecosystem over XML for FIX Repository. As a proof of concept, I am releasing FIX2dict.

# Introduction to FIX2dict

FIX2dict is a collection of related tools to read, update, modify FIX Repository data. First and foremost, it allows you to transform original FIX Repository data (i.e. `.xml`) into JSON. A standard-compliant [JSON Schema](https://json-schema.org/) description describes the format of produced data. This way, a lot of jobs can become much easier:

- Code generation. FIX2dict supersedes software like [`fix-repository-to-quickfix-xml`](https://code.google.com/archive/p/fix-repository-to-quickfix-xml/).
- Documentation generation. Programmatic generation of both high-quality documentation files (in formats like `.pdf`, `.doc`) and browser-oriented tools becomes much easier. A proof of concept is currently in the works.

# About Extension Packs

FIX2dict can also transform EP files (`.xml`) into a [JSON Patch](https://tools.ietf.org/html/rfc6902) file. We can leverage JSON Patch -already standardized by W3C- to completely remove the need for XSLT scripts and DDT

# Conclusions

I welcome feedback and I remain available for further clarifications. You can contact me at my personal email address [`filippocosta.italy@gmail.com`](mailto:filippocosta.italy@gmail.com). Hopefully members of the FIX Trading Community will see this as a great opportunity for lowering the barrier of access to the FIX Repository, which is at the heart of any serious tool for FIX.

Finally, just as a powerful example of what can be readily achieved with high-quality FIX Repository data, you can have a look at [fixipe.com](https://fixipe.com). It was built leveraging FIX2dict's features and, with some more work, it could work great not only as online FIX Dictionary but also as editor, allowing people to create custom EPs and then export them in multiple formats.