# Protocol Documentation
<a id="top"></a>

## Table of Contents

- [bookclub/book.proto](#bookclub_book-proto)
    - [Book](#bookclub-Book)
  
    - [GENRE](#bookclub-GENRE)
  
- [bookclub/member.proto](#bookclub_member-proto)
    - [Member](#bookclub-Member)
    - [Member.RatingsEntry](#bookclub-Member-RatingsEntry)
  
- [bookclub/bookclub.proto](#bookclub_bookclub-proto)
    - [Bookclub](#bookclub-Bookclub)
    - [GetMembersRequest](#bookclub-GetMembersRequest)
    - [GetMembersResponse](#bookclub-GetMembersResponse)
  
    - [BookclubGRPC](#bookclub-BookclubGRPC)
  
- [Scalar Value Types](#scalar-value-types)



<a id="bookclub_book-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## bookclub/book.proto



<a id="bookclub-Book"></a>

### Book



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| bookname | [string](#string) |  |  |
| author_name | [string](#string) |  |  |
| num_of_pages | [int32](#int32) |  |  |
| publication_date | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |  |  |
| genres | [GENRE](#bookclub-GENRE) | repeated |  |
| bookID | [string](#string) |  |  |





 


<a id="bookclub-GENRE"></a>

### GENRE


| Name | Number | Description |
| ---- | ------ | ----------- |
| GENRE_COMEDY | 0 |  |
| GENRE_ROMANCE | 1 |  |
| GENRE_DETECTIVE | 2 |  |


 

 

 



<a id="bookclub_member-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## bookclub/member.proto



<a id="bookclub-Member"></a>

### Member



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| ID | [string](#string) |  |  |
| age | [int32](#int32) |  |  |
| read_books | [Book](#bookclub-Book) | repeated |  |
| ratings | [Member.RatingsEntry](#bookclub-Member-RatingsEntry) | repeated | book ratings, bookID is key |






<a id="bookclub-Member-RatingsEntry"></a>

### Member.RatingsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [float](#float) |  |  |





 

 

 

 



<a id="bookclub_bookclub-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## bookclub/bookclub.proto



<a id="bookclub-Bookclub"></a>

### Bookclub



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| members | [Member](#bookclub-Member) | repeated |  |
| description | [string](#string) |  |  |
| books | [Book](#bookclub-Book) | repeated |  |






<a id="bookclub-GetMembersRequest"></a>

### GetMembersRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| age_range_low | [int32](#int32) |  |  |
| age_range_high | [int32](#int32) |  |  |






<a id="bookclub-GetMembersResponse"></a>

### GetMembersResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| members | [Member](#bookclub-Member) | repeated |  |





 

 

 


<a id="bookclub-BookclubGRPC"></a>

### BookclubGRPC


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetMembers | [GetMembersRequest](#bookclub-GetMembersRequest) | [GetMembersResponse](#bookclub-GetMembersResponse) |  |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a id="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a id="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a id="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a id="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a id="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a id="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a id="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a id="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a id="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a id="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a id="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a id="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a id="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a id="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a id="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

