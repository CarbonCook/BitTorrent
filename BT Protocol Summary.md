# BitTorrent Protocol Summary


## Bencoding
The encoding of metainfo files.

### Syntax Convention
* [_Dict_] stands for Bencoding Dictionary.
* [_List_] stands for Bencoding List.
* [_Str_] stands for Bencoding String.
* [_Int_] stands for Bencoding Integer.
* [_Val_] stands for any element above.
* [s] stands for string.
* [i] stands for integer.
* \* stands for 0 or more repetitions of the preceding element.
  * **eg.** [_Str_]* means 0 or more repetitions of [_Str_].

### Bencoding
1. Dictionry format
   * d([_Str_][_Val_])*e
2. List format
   * l[_Val_]*e
3. String format (where [i] represents the length of [s])
   * \[i\]:[s]
4. Integer format
   * i[i]e


## Metainfo File
An bencoded dictionary (known as .torrent file).
All text strings must be UTF-8 encoded.

### Main Keys
**announce** The URL of the tracker.  
**info** The dictionary on info of files.

* **name** The suggested name to save the file (or directory) as.
* **files** The list of file dictionaries. If there's only one file, the items in the file dictionary will be exposed directly as the items of **info**. Below are main keys of file dictionary:

  * **length** The length of the file in bytes.
  * **path** The subdirectory names of the file.

**piece length** The number of bytes in each piece the file is split into.  
**pieces** A string that can be subdivided into strings of length 20, each of which is the SHA1 hash of the piece at the corresponding index.


## Tracker
### Keys in GET Requests
**info_hash** The 20 byte sha1 hash of the bencoded form of the info value from the metainfo file. (Escaped)  
**peer_id** A string of length 20 which downloader generates as its id at random at the start of a new download. (Escaped)  
**ip** IP or DNS name which the peer is at. (Optional)  
**port** The port numner the peer (downloader) is listen on, usually between 6881 and 6889.  
**uploaded** The total amount uploaded so far, encoded in base ten ascii.  
**downloaded** The total amount downloaded so far, encoded in base ten ascii.  
**left** The number of bytes this peer still has to download, encoded in base ten ascii.  
**event** An optional key which maps to _started_, _completed_ or _stopped_ (or empty which indicates one of the announcements done at regular intervals)  
**compact** _compact=0_ indicates that the becoded format is preferred, and analogously _compact=1_ advises the tracker that the client prefers compact format. (See the following part for more information.)

### Response Dictionary (bencoded)
Some possible keys:  
**failure reason** A human readable string which explains why the query failed.  
**interval** The number of seconds the downloader should wait between regular rerequests.  
**peers** A list of dictionaries corresponding to peers. Each dictionary contains three keys:

* **peer id** The peer's self-selected ID.
* **ip** IP address or dns name as a string.
* **port** Port number.

Note that in addition to the bencoded format for each peer in **peers**, the compact string format is advisory, where each peer is represented using only 6 bytes. The first 4 bytes contains 32-bit ipv4 address and the remaining 2 bytes contains the port number. Both of them use [network-byte order](https://en.wikipedia.org/wiki/Endianness#Big-endian).

### Related Reading
1. [BEP 23](http://www.bittorrent.org/beps/bep_0023.html), _Tracker Returns Compact Peer Lists_
2. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), _UDP Tracker Protocol for BitTorrent_


## Peer Protocol
BitTorrent's peer protocol operates over TCP or [uTP](http://www.bittorrent.org/beps/bep_0029.html).  



## References
1. [BEP 3](http://www.bittorrent.org/beps/bep_0003.html), _The BitTorrent Protocol Specification_, Bram Cohen, 10-Jan-2008