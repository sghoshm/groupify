import 'package:flutter/material.dart';
import 'package:groupify/pages/chat_page.dart';

class GroupInfo extends StatefulWidget {
  final String groupId;
  final String groupName;
  final String adminName;
  const GroupInfo(
      {Key? key,
      required this.adminName,
      required this.groupId,
      required this.groupName})
      : super(key: key);

  @override
  State<GroupInfo> createState() => _GroupInfoState();
}

class _GroupInfoState extends State<GroupInfo> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Group Info"),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Theme.of(context).primaryColor,
        actions: [IconButton(onPressed: () {}, icon: Icon(Icons.group_off))],
      ),
      body: Center(
        child: Text(widget.adminName),
      ),
    );
  }
}
