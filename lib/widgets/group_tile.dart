import 'package:flutter/material.dart';
import 'package:groupify/widgets/widgets.dart';

import '../pages/chat_page.dart';

class GroupTile extends StatefulWidget {
  final String userName;
  final String groupName;
  final String groupId;
  const GroupTile(
      {Key? key,
      required this.groupId,
      required this.groupName,
      required this.userName})
      : super(key: key);

  @override
  State<GroupTile> createState() => _GroupTileState();
}

class _GroupTileState extends State<GroupTile> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
        onTap: () {
          nextScreen(
              context,
              ChatPage(
                groupId: widget.groupId,
                groupName: widget.groupName,
                userName: widget.userName,
              ));
        },
        child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            child: ListTile(
              leading: CircleAvatar(
                radius: 30,
                backgroundColor: Theme.of(context).primaryColor,
                child: Text(widget.groupName.substring(0, 1).toUpperCase(),
                    style: const TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.bold)),
              ),
              title: Text(widget.groupName,
                  style: const TextStyle(
                      color: Colors.black,
                      fontSize: 20,
                      fontWeight: FontWeight.bold)),
              subtitle: Text(
                "Join as ${widget.userName}",
              ),
            )));
  }
}
